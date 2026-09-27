# instagram-engagement-scraper
# 🚀 Viral Trend Analyst (Instagram Engagement Scraper)

An end-to-end automated data engineering pipeline designed to extract, process, and visualize the most highly engaged Instagram Reels for any given keyword. Built to streamline social media research and marketing intelligence by replacing manual scrolling with a programmatic, data-driven approach.

## 🎥 Project Demo
<!-- DRAG AND DROP YOUR DEMO VIDEO (.mp4) RIGHT HERE -->

## 📸 Dashboard Preview
<!-- DRAG AND DROP YOUR DASHBOARD SCREENSHOT RIGHT HERE -->

---

## ⚙️ System Architecture

<!-- DRAG AND DROP YOUR FLOWCHART IMAGE RIGHT HERE -->

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
     ▪ Generates interactive metric cards & direct Reel links<img width="1461" height="792" alt="Screenshot 2026-09-27 014907" src="https://github.com/user-attachments/assets/5552ff45-5059-4d0d-8e62-6c18dd1e7d86" />
