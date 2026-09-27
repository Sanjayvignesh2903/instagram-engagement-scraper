import streamlit as st
import pandas as pd
from agent import app as agent_app

# --- Page Configuration ---
st.set_page_config(
    page_title="Viral Trend Analyst",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Custom Dark Aesthetic Styling ---
st.markdown("""
    <style>
        .stApp {
            background-color: #0c0c0c;
            color: #fafafa;
        }
        .main-title {
            text-align: center;
            font-size: 2.8rem;
            font-weight: 600;
            background: -webkit-linear-gradient(45deg, #feda75, #fa7e1e, #d62976, #962fbf);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.2rem;
        }
        .sub-title {
            text-align: center;
            color: #9e9e9e;
            font-size: 1.1rem;
            margin-bottom: 2rem;
        }
        .metric-card {
            background: #161616;
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 12px;
            padding: 20px;
            text-align: center;
            margin-bottom: 15px;
        }
        .metric-card h3 {
            color: #fa7e1e;
            margin-bottom: 5px;
        }
        .reel-link {
            display: inline-block;
            margin-top: 10px;
            padding: 6px 14px;
            background: linear-gradient(45deg, #feda75, #fa7e1e, #d62976);
            color: #fff !important;
            text-decoration: none;
            border-radius: 20px;
            font-weight: 500;
            font-size: 0.85rem;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">Spot the trend. Break the internet.</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Set your parameters or describe your vision. The AI will extract the most viral matches.</div>', unsafe_allow_html=True)

# --- Input Section ---
with st.container():
    col_input, _ = st.columns([1, 0.01])
    with col_input:
        custom_prompt = st.text_area(
            "Describe your vision (Optional)",
            placeholder="e.g., emotional dark theme tamil song or an aggressive mass edit..."
        )

    col1, col2 = st.columns(2)
    with col1:
        theme = st.selectbox(
            "Video Theme / Vibe (Optional)",
            ["", "Emotional & Cinematic", "Aggressive / Angry", "Hustle & Motivation", "Dark Aesthetic", "Fast-Paced Hype"]
        )
        scope = st.selectbox("Region Scope (Optional)", ["Global", "Specific Location"])
        
    with col2:
        if scope == "Specific Location":
            location = st.text_input("Nation / State", placeholder="e.g., Tamil Nadu")
        else:
            location = ""
            
        language = st.text_input("Language Focus (Optional)", placeholder="e.g., Tamil")

    metric = st.selectbox("Optimization Goal", ["Maximize Likes", "Maximize Comments"])
    
    submit = st.button("Extract Viral Trends", use_container_width=True)

# --- Analysis Execution & Results ---
if submit:
    # 1. Build dynamic query
    prompt_parts = []
    if custom_prompt:
        prompt_parts.append(f"User Vision: {custom_prompt}")
    if theme:
        prompt_parts.append(f"Vibe: {theme}")
    if language:
        prompt_parts.append(f"Language: {language}")
    if location:
        prompt_parts.append(f"Region: {location}")
        
    user_prompt = " | ".join(prompt_parts)
    if not user_prompt:
        user_prompt = "Find top globally trending viral reels"

    with st.spinner("AI Agents analyzing parameters and pulling live Instagram data via Apify..."):
        initial_state = {
            "user_prompt": user_prompt,
            "search_type": "",
            "search_query": "",
            "raw_data": [],
            "recommendation": ""
        }
        
        try:
            final_state = agent_app.invoke(initial_state)
            raw_live_reels = final_state.get("raw_data", [])
        except Exception as e:
            st.error(f"Live scrape failed: {e}")
            raw_live_reels = []

        # Filter low-engagement noise
        viral_reels = [r for r in raw_live_reels if r.get("like_count", 0) > 50]
        if not viral_reels:
            viral_reels = raw_live_reels

        # Sort according to selected metric
        if metric == "Maximize Comments":
            sorted_reels = sorted(viral_reels, key=lambda x: x.get("comment_count", 0), reverse=True)
        else:
            sorted_reels = sorted(viral_reels, key=lambda x: x.get("like_count", 0), reverse=True)

        top_5 = sorted_reels[:5]

    if top_5:
        st.subheader("Top 5 Viral Candidates")
        
        # Display cards
        cols = st.columns(len(top_5))
        chart_data = []
        
        for idx, (c, reel) in enumerate(zip(cols, top_5)):
            likes = reel.get("like_count", 0)
            comments = reel.get("comment_count", 0)
            views = reel.get("playCount") or (likes * 12)
            url = reel.get("url", "https://instagram.com")
            
            with c:
                st.markdown(f"""
                <div class="metric-card">
                    <p style="color:#888; font-size: 0.85rem; margin:0;">Rank #{idx + 1}</p>
                    <h3>{views/1_000_000:.1f}M</h3>
                    <p style="color:#aaa; font-size: 0.8rem; margin:0;">Est. Views</p>
                    <p style="color:#d62976; margin: 8px 0 0 0;">❤️ {likes:,}</p>
                    <p style="color:#feda75; margin: 2px 0 0 0;">💬 {comments:,}</p>
                    <a href="{url}" target="_blank" class="reel-link">View Reel</a>
                </div>
                """, unsafe_allow_html=True)
                
            chart_data.append({
                "Post": f"Rank #{idx + 1}",
                "Likes": likes,
                "Comments": comments
            })

        # Display Comparison Chart
        st.markdown("---")
        st.subheader("Engagement Distribution")
        df = pd.DataFrame(chart_data)
        st.bar_chart(df.set_index("Post")[["Likes", "Comments"]])
    else:
        st.warning("No high-engagement reels found matching this specific query. Try a broader search or popular creator username.")