# 🚀 Viral Trend Analyst (Instagram Engagement Scraper)

An end-to-end automated data engineering pipeline designed to extract, process, and visualize the most highly engaged Instagram Reels for any given keyword. Built to streamline social media research and marketing intelligence by replacing manual scrolling with a programmatic, data-driven approach.

## 🎥 Project Demo
<video src="Screen%20Recording%202026-09-27%20011602.mp4" controls="controls" style="max-width: 100%;"></video>

## 📸 Dashboard Preview
![Dashboard Preview](Screenshot%202026-09-27%20014907.png)

---

## ⚙️ System Architecture

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
```

🛠️ Tech Stack
Backend: Python, FastAPI, Uvicorn, Pydantic

Data Extraction: Apify API (crawlerbros/instagram-keyword-scraper)

Database: Supabase (PostgreSQL), supabase-py

Frontend: HTML5, CSS3, Vanilla JavaScript, Chart.js

🧠 Core Features & Logic
Algorithmic Sorting: Bypasses standard chronological platform feeds to isolate historical, all-time high-engagement outliers.

Database Integrity: Utilizes PostgreSQL UPSERT operations (ON CONFLICT) mapping to Instagram shortcodes to prevent duplicate warehouse records.

Dynamic Estimation: Implements fallback logic to calculate estimated views when raw payload metadata is missing playCount fields.

Interactive UI: Features asynchronous Fetch API polling, Chart.js data visualization, and hardware-accelerated CSS animations (fluid cursor trails, gradient edge-loaders).
