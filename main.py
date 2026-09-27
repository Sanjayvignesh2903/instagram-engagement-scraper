import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional
import uvicorn
from dotenv import load_dotenv
from supabase import create_client, Client
from apify_client import ApifyClient

# Load Environment Variables
load_dotenv()

# Initialize App and Clients
app = FastAPI()
supabase: Client = create_client(os.environ.get("SUPABASE_URL"), os.environ.get("SUPABASE_KEY"))
apify_client = ApifyClient(os.environ.get("APIFY_API_TOKEN"))

class TrendQuery(BaseModel):
    custom_prompt: Optional[str] = ""
    theme: Optional[str] = ""
    metric: Optional[str] = "Likes"

@app.get("/", response_class=HTMLResponse)
async def serve_ui():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/api/analyze")
async def analyze_trends(query: TrendQuery):
    # 1. Determine keyword (default to #tamillovesongs if empty)
    keyword = query.custom_prompt.strip() if query.custom_prompt else "#tamillovesongs"
    if not keyword.startswith("#"):
        keyword = f"#{keyword}"
        
    print(f"\n[Scraper] Starting live extraction for {keyword}...")
    
    # 2. Scrape Live Data from Apify
    run_input = {
        "keywords": [keyword],
        "maxPosts": 30
    }
    
    try:
        run = apify_client.actor("crawlerbros/instagram-keyword-scraper").call(run_input=run_input)
        dataset_id = run.default_dataset_id
        dataset = list(apify_client.dataset(dataset_id).iterate_items())
    except Exception as e:
        print(f"[Error] Apify Scrape Failed: {e}")
        return {"status": "error", "message": "Scraper failed."}

    reels = []
    
    # 3. Clean and Format Data
    for item in dataset:
        likes = item.get("like_count") or 0
        comments = item.get("comment_count") or 0
        url = item.get("post_url")
        
        shortcode = ""
        if url:
            parts = url.rstrip("/").split("/")
            if len(parts) > 0:
                shortcode = parts[-1]
                
        if shortcode and url:
            reels.append({
                "shortcode": shortcode,
                "url": url,
                "caption": str(item.get("caption", ""))[:200],
                "like_count": int(likes),
                "comment_count": int(comments)
            })
            
    # 4. Isolate the Absolute Top 5 by Likes
    sorted_reels = sorted(reels, key=lambda x: x["like_count"], reverse=True)
    top_5_reels = sorted_reels[:5]
            
    # 5. Save to Supabase (Upsert prevents duplicates)
    if top_5_reels:
        try:
            print(f"[Database] Saving {len(top_5_reels)} viral reels to Supabase...")
            supabase.table("reels").upsert(top_5_reels, on_conflict="shortcode").execute()
        except Exception as e:
            print(f"[Error] Supabase Upsert Failed: {e}")
            
    # 6. Format Payload for Frontend Rendering
    formatted_posts = []
    for item in top_5_reels:
        likes = item.get("like_count") or 0
        comments = item.get("comment_count") or 0
        views = likes * 14  # Estimated views based on engagement ratio
        
        formatted_posts.append({
            "url": item.get("url"),
            "likes": int(likes),
            "comments": int(comments),
            "views": int(views)
        })

    print("[Success] Data pipeline complete. Returning to UI.")
    return {
        "status": "success",
        "top_posts": formatted_posts
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)