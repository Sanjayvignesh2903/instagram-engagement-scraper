# 🚀 Viral Trend Analyst (Instagram Engagement Scraper)

An end-to-end automated data engineering pipeline designed to extract, process, and visualize the most highly engaged Instagram Reels for any given keyword. Built to streamline social media research and marketing intelligence by replacing manual scrolling with a programmatic, data-driven approach.

## 🎥 Project Demo

<video src="Demo_video" controls="controls" style="max-width: 100%;"></video>

*(If the video player does not load above, [click here to watch the Demo Video](Demo_video))*

---

## ⚙️ System Architecture

![System Architecture](architecture%20diagram)

```text
📱 [ Frontend UI (HTML/CSS/JS/Chart.js) ]
 │   ▪ Captures parameters & displays interactive loaders
 ▼
⚡ [ FastAPI Backend (Python) ]
 │   ▪ Orchestrates the data extraction pipeline
 ▼
🕷️ [ Apify Keyword Scraper ]
 │   ▪ Bypasses blocks to dynamically scrape high-engagement posts
 ▼
⚙️ [ Data Processing Engine ]
 │   ▪ Cleans metrics, estimates views, and isolates the Top 5 hits
 ▼
🗄️ [ Supabase (PostgreSQL) ]
 │   ▪ Upserts data safely, preventing duplicates via shortcode IDs
 ▼
📊 [ Dynamic Dashboard Rendering ]
     ▪ Generates interactive metric cards & direct Reel links
