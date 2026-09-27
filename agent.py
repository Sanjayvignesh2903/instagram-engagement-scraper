import os
from typing import TypedDict, List
from dotenv import load_dotenv
from supabase import create_client, Client
from apify_client import ApifyClient
from langgraph.graph import StateGraph, START, END

load_dotenv()
supabase: Client = create_client(os.environ.get("SUPABASE_URL"), os.environ.get("SUPABASE_KEY"))
apify_client = ApifyClient(os.environ.get("APIFY_API_TOKEN"))

class AgentState(TypedDict):
    user_prompt: str
    search_query: str
    raw_data: List[dict]
    recommendation: str

def generate_search_query(state: AgentState) -> AgentState:
    print(f"\n[Agent] Targeting hashtag: #tamillovesongs")
    return {"search_query": "tamillovesongs"}

def live_scrape_data(state: AgentState) -> AgentState:
    tag = state["search_query"]
    print(f"[Scraper] Connecting to Apify to pull reels for #{tag}...")

    # Using the dedicated reel scraper actor
    run_input = {
        "hashtags": [tag],
        "resultsLimit": 25
    }
        
    dataset_items = []
    try:
        run = apify_client.actor("apify/instagram-reel-scraper").call(run_input=run_input)
        dataset_items = list(apify_client.dataset(run.get("defaultDatasetId")).iterate_items())
    except Exception as e:
        print(f"[Scraper] Primary reel scraper error: {e}, trying fallback actor...")
        try:
            # Fallback to general instagram scraper if reel scraper fails
            run = apify_client.actor("apify/instagram-scraper").call(run_input=run_input)
            dataset_items = list(apify_client.dataset(run.get("defaultDatasetId")).iterate_items())
        except Exception as err:
            print(f"[Scraper] Fallback failed too: {err}")

    reels_to_insert = []
    for item in dataset_items:
        # Extract metrics safely across different Apify output formats
        likes = item.get("likesCount") or item.get("likes") or 0
        comments = item.get("commentsCount") or item.get("comments") or 0
        views = item.get("videoPlayCount") or item.get("videoViewCount") or item.get("playCount") or (likes * 12)
        
        # Build clean URL
        shortcode = item.get("shortCode") or item.get("code") or item.get("id")
        url = item.get("url")
        if not url and shortcode:
            url = f"https://www.instagram.com/reel/{shortcode}/"
            
        if url and shortcode:
            reels_to_insert.append({
                "shortcode": str(shortcode),
                "url": url,
                "caption": item.get("caption", ""),
                "like_count": int(likes),
                "comment_count": int(comments),
                "playCount": int(views)
            })

    print(f"[Scraper] Extracted {len(reels_to_insert)} valid items.")

    # FORCE INSERTION INTO SUPABASE
    if reels_to_insert:
        try:
            print(f"[Supabase] Inserting {len(reels_to_insert)} reels into database...")
            supabase.table("reels").upsert(reels_to_insert, on_conflict="shortcode").execute()
            print("[Supabase] Data successfully saved!")
        except Exception as db_err:
            print(f"[Supabase] Error saving data: {db_err}")

    return {"raw_data": reels_to_insert}

def analyze_trends(state: AgentState) -> AgentState:
    return {"recommendation": "Analysis Complete"}

workflow = StateGraph(AgentState)
workflow.add_node("Supervisor", generate_search_query)
workflow.add_node("Scraper", live_scrape_data)
workflow.add_node("Analyst", analyze_trends)

workflow.add_edge(START, "Supervisor")
workflow.add_edge("Supervisor", "Scraper")
workflow.add_edge("Scraper", "Analyst")
workflow.add_edge("Analyst", END)

app = workflow.compile()