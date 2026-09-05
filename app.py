import os
import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page Configuration & Professional Styling Layout
st.set_page_config(
    page_title="Generosity & Empathy Platform", 
    page_icon="🌟", 
    layout="wide"
)

# Custom Global CSS for Rich SaaS/Non-Profit Styling
st.markdown("""
    <style>
    .stApp {
        background-color: #F8FAFC;
    }
    .main-header {
        font-size: 2.4rem;
        color: #0F172A;
        font-weight: 800;
        letter-spacing: -0.03em;
        margin-bottom: 0px;
    }
    .sub-title {
        font-size: 1.05rem;
        color: #475569;
        font-weight: 500;
        margin-bottom: 20px;
    }
    .card-box {
        background-color: #FFFFFF;
        padding: 24px;
        border-radius: 16px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
    }
    .stButton button {
        background: linear-gradient(135deg, #4F46E5 0%, #3B82F6 100%);
        color: white;
        border-radius: 10px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        border: none;
        box-shadow: 0 4px 14px rgba(79, 70, 229, 0.2);
        transition: all 0.3s ease;
    }
    .stButton button:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 20px rgba(79, 70, 229, 0.3);
    }
    .footer {
        text-align: center;
        color: #94A3B8;
        font-size: 0.85rem;
        margin-top: 50px;
        padding: 25px;
        border-top: 1px solid #E2E8F0;
    }
    </style>
""", unsafe_allow_html=True)

# Define Multi-page Navigation
pg = st.navigation([
    st.Page("pages/1_🤝_Matchmaker.py", title="AI Matchmaker", icon="🤝"),
    st.Page("pages/2_📊_Impact_Logs.py", title="Cloud Impact Logs", icon="📊"),
    st.Page("pages/3_ℹ️_About_Mission.py", title="About Our Mission", icon="ℹ️")
])

# Run the selected page
pg.run()

# Persistent Global Footer
st.markdown("""
    <div class="footer">
        🌟 Generosity & Empathy Network • Powered by Google Gemini AI, ElevenLabs, Solana & Snowflake • Cultivating Global Kindness.
    </div>
""", unsafe_allow_html=True)
