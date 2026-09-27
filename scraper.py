import os
from apify_client import ApifyClient
from supabase import create_client, Client
from dotenv import load_dotenv

# 1. Load your secret keys from the .env file
load_dotenv()

# 2. Initialize the Apify and Supabase clients
apify_client = ApifyClient(os.environ.get("APIFY_API_TOKEN"))

supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

def fetch_and_store_reels(target_username: str):
    print(f"Starting scraper for @{target_username}...")
    
    # 3. Call the OFFICIAL Apify scraper
    run_input = {
        "username": [target_username], # FIXED: 'username' instead of 'usernames'
        "resultsLimit": 10  # Pull only the latest 10 to test quickly
    }
    
    run = apify_client.actor("apify/instagram-reel-scraper").call(run_input=run_input)
    
    # 4. Fetch the raw JSON results from Apify
    dataset = apify_client.dataset(run.default_dataset_id).iterate_items()
    
    reels_to_insert = []
    
    # 5. Format the data to match our Supabase table
    for item in dataset:
        reel_record = {
            "shortcode": str(item.get("id")),
            "url": item.get("url"),
            "caption": item.get("caption"),
            "like_count": item.get("likesCount"),
            "comment_count": item.get("commentsCount"),
            "timestamp": item.get("timestamp")
        }
        reels_to_insert.append(reel_record)
            
    if reels_to_insert:
        print(f"Found {len(reels_to_insert)} Reels. Saving to database...")
        # 6. Insert data into Supabase  
        response = supabase.table("reels").upsert(
            reels_to_insert, 
            on_conflict="shortcode"
        ).execute()
        
        print(f"Success! Data saved.")
    else:
         print("No Reels found for this account.")

if __name__ == "__main__":
    fetch_and_store_reels("#tamillovesongs")  # Example usage with a hashtag