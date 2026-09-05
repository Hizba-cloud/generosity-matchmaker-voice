import os
import streamlit as st
from google import genai
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
import qrcode
from io import BytesIO
import snowflake.connector
import pandas as pd

# Load environment variables
load_dotenv()

# Initialize Clients securely
client = genai.Client()
eleven_client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))

# Function to log impact data to Snowflake
def log_to_snowflake(user_input, category):
    try:
        conn = snowflake.connector.connect(
            user=os.getenv("SNOWFLAKE_USER"),
            password=os.getenv("SNOWFLAKE_PASSWORD"),
            account=os.getenv("SNOWFLAKE_ACCOUNT"),
            warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
            database=os.getenv("SNOWFLAKE_DATABASE"),
            schema=os.getenv("SNOWFLAKE_SCHEMA")
        )
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS generosity_logs (
                timestamp TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
                user_contribution STRING,
                charity_category STRING
            )
        """)
        cursor.execute(
            "INSERT INTO generosity_logs (user_contribution, charity_category) VALUES (%s, %s)",
            (user_input, category)
        )
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Snowflake Logging Info: {e}")

# App Page Configuration
st.set_page_config(
    page_title="Generosity & Empathy Matchmaker", 
    page_icon="🌟", 
    layout="wide"
)

# Custom Styling for Professional SaaS Look
st.markdown("""
    <style>
    .stApp {
        background-color: #F8FAFC;
    }
    .main-header {
        font-size: 2.5rem;
        color: #0F172A;
        font-weight: 800;
        letter-spacing: -0.03em;
        margin-bottom: 5px;
    }
    .sub-title {
        font-size: 1.1rem;
        color: #475569;
        font-weight: 500;
        margin-bottom: 25px;
    }
    .card-container {
        background-color: #FFFFFF;
        padding: 30px;
        border-radius: 20px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        margin-bottom: 25px;
    }
    .stButton button {
        background: linear-gradient(135deg, #4F46E5 0%, #3B82F6 100%);
        color: white;
        border-radius: 12px;
        padding: 0.6rem 1.2rem;
        font-weight: 600;
        border: none;
        box-shadow: 0 4px 14px rgba(79, 70, 229, 0.25);
        transition: all 0.3s ease;
    }
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(79, 70, 229, 0.35);
    }
    div[data-baseweb="textarea"] textarea {
        background-color: #FFFFFF;
        border-radius: 14px;
        border: 1px solid #CBD5E1;
        padding: 16px;
        color: #1E293B;
        font-size: 1rem;
    }
    .footer {
        text-align: center;
        color: #94A3B8;
        font-size: 0.9rem;
        margin-top: 60px;
        padding: 25px;
        border-top: 1px solid #E2E8F0;
    }
    </style>
""", unsafe_allow_html=True)

# App Header Section
st.markdown('<p class="main-header">🌟 Generosity & Empathy Matchmaker</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Connecting human kindness with verified community causes through Gemini AI, ElevenLabs, Solana & Snowflake.</p>', unsafe_allow_html=True)

# Modern Tab Navigation
tab1, tab2, tab3 = st.tabs(["🤝 AI Matchmaker", "📊 Impact Telemetry Logs", "ℹ️ Mission & About"])

# ================= TAB 1: MATCHMAKER DASHBOARD =================
with tab1:
    col_main, col_side = st.columns([1.4, 1], gap="large")

    with col_main:
        st.markdown('<div class="card-container">', unsafe_allow_html=True)
        st.markdown("### 📝 Share Your Contribution")
        st.info("💡 **How it works:** Choose a quick-select cause below or type your custom offering to build an instant action plan.")

        if "input_text" not in st.session_state:
            st.session_state["input_text"] = ""

        st.markdown("**Quick-Select Popular Causes:**")
        q1, q2, q3, q4 = st.columns(4)
        with q1:
            if st.button("🧥 Jackets", use_container_width=True):
                st.session_state["input_text"] = "I have 5 old winter jackets and blankets to donate for the cold season."
        with q2:
            if st.button("📚 Books", use_container_width=True):
                st.session_state["input_text"] = "I have a collection of children's storybooks and notebooks to share."
        with q3:
            if st.button("🍲 Food", use_container_width=True):
                st.session_state["input_text"] = "I want to donate non-perishable food supplies and dry rations for a local food drive."
        with q4:
            if st.button("💻 Tutoring", use_container_width=True):
                st.session_state["input_text"] = "I want to volunteer 2 hours a week teaching basic coding and math to kids."

        with st.form("match_form"):
            user_input = st.text_area(
                "What would you like to donate or contribute?",
                value=st.session_state["input_text"],
                placeholder="e.g., I want to volunteer time or donate items...",
                height=130
            )
            submit_button = st.form_submit_button("Generate AI Impact Roadmap ✨", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_side:
        st.markdown('<div class="card-container">', unsafe_allow_html=True)
        st.markdown("### 🌍 Cultivating Global Empathy")
        st.image(
            "https://images.unsplash.com/photo-1593113598332-cd288d649433?auto=format&fit=crop&w=600&q=80",
            use_container_width=True,
            caption="Empowering community-driven impact."
        )
        st.markdown("""
        * **✨ Tailored Guidance:** Crafted intelligently via Google Gemini.
        * **🎙️ Voice Accessible:** Custom audio guides via ElevenLabs.
        * **🪙 Transparent Routing:** Tracked securely via Snowflake & Solana.
        """)
        st.markdown('</div>', unsafe_allow_html=True)

    # Handle Submission
    if submit_button:
        if not user_input.strip():
            st.warning("⚠️ Please enter or select what you'd like to contribute first!")
        else:
            with st.spinner("✨ Consulting Gemini AI to map your impact roadmap..."):
                try:
                    prompt = f"""
                    You are an empathetic AI assistant for a global charity and community generosity platform. 
                    A user wants to give back and has provided this input: "{user_input}"
                    
                    Please respond cleanly with:
                    1. **Recommended Category of Charity/Cause:** (e.g., Education, Warmth/Clothing Drive, Food Security)
                    2. **How to Prepare Items/Time:** (3 brief bullet points on what the user should do next)
                    3. **Suggested Platforms or Search Terms:** (Provide 2-3 types of verified organizations, platforms, or search queries they can use to find active drives or direct donation links nearby)
                    4. **Drafted Outreach Message:** (A short, polite message the user can copy-paste to a local shelter, NGO, or community center)
                    """

                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=prompt,
                    )
                    
                    st.session_state["match_result"] = response.text
                    st.session_state["input_given"] = user_input
                    log_to_snowflake(user_input, "General Match")

                except Exception as e:
                    st.error(f"An error occurred with Gemini: {e}")

    # Display Results if generated
    if "match_result" in st.session_state:
        st.markdown("---")
        res_col1, res_col2 = st.columns(2, gap="large")
        
        with res_col1:
            st.markdown('<div class="card-container">', unsafe_allow_html=True)
            st.markdown("### 📋 Your Action Plan")
            st.markdown(st.session_state["match_result"])
            st.markdown('</div>', unsafe_allow_html=True)

        with res_col2:
            st.markdown('<div class="card-container">', unsafe_allow_html=True)
            st.markdown("### 🎙️ Audio Voice Guide")
            st.write("Listen to your generated impact guide read aloud by ElevenLabs.")
            if st.button("🔊 Play Voice Synthesis", use_container_width=True):
                with st.spinner("Synthesizing audio stream..."):
                    try:
                        tts_script = (
                            "Here is your personalized generosity match guide. "
                            f"Based on your contribution of: {st.session_state['input_given']}. "
                            f"Here is the plan: {st.session_state['match_result']}"
                        )
                        audio_stream = eleven_client.text_to_speech.convert(
                            text=tts_script,
                            voice_id="21m00Tcm4TlvDq8ikWAM",
                            model_id="eleven_multilingual_v2",
                            output_format="mp3_44100_128",
                        )
                        audio_bytes = b"".join(list(audio_stream))
                        st.audio(audio_bytes, format="mp3")
                        st.success("Audio ready!")
                    except Exception as e:
                        st.error(f"ElevenLabs Error: {e}")

            st.markdown("---")
            st.markdown("### 🪙 Solana Micro-Donations")
            wallet_address = "GenerosityFundSolanaWallet11111111111111"
            st.code(wallet_address, language="text")
            
            try:
                qr = qrcode.QRCode(version=1, box_size=6, border=2)
                qr.add_data(wallet_address)
                qr.make(fit=True)
                img = qr.make_image(fill_color="black", back_color="white")
                buffered = BytesIO()
                img.save(buffered, format="PNG")
                st.image(buffered.getvalue(), width=160, caption="Scan via Phantom / Solflare")
            except Exception:
                pass
            st.markdown('</div>', unsafe_allow_html=True)

# ================= TAB 2: SNOWFLAKE LOGS =================
with tab2:
    st.markdown('<div class="card-container">', unsafe_allow_html=True)
    st.markdown("### 📊 Cloud Telemetry Warehouse")
    st.write("Fetching real-time engagement and submission records securely captured from the Snowflake database (`generosity_logs`).")
    
    try:
        conn = snowflake.connector.connect(
            user=os.getenv("SNOWFLAKE_USER"),
            password=os.getenv("SNOWFLAKE_PASSWORD"),
            account=os.getenv("SNOWFLAKE_ACCOUNT"),
            warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
            database=os.getenv("SNOWFLAKE_DATABASE"),
            schema=os.getenv("SNOWFLAKE_SCHEMA")
        )
        df = pd.read_sql("SELECT * FROM generosity_logs ORDER BY timestamp DESC LIMIT 50", conn)
        conn.close()
        
        if not df.empty:
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No logs recorded yet. Submit a match on the Matchmaker tab to populate this telemetry table!")
    except Exception as e:
        st.warning(f"Could not connect to Snowflake to render the live table in preview: {e}")
        st.info("You can run this query directly in your Snowflake worksheet:\n`SELECT * FROM generosity_db.public.generosity_logs ORDER BY timestamp DESC;`")
    st.markdown('</div>', unsafe_allow_html=True)

# ================= TAB 3: ABOUT MISSION =================
with tab3:
    st.markdown('<div class="card-container">', unsafe_allow_html=True)
    st.markdown("### 🌟 About Our Empathy Mission")
    st.markdown("""
    In a world full of resources and people willing to give back, the biggest barrier is friction—not knowing **where** items are needed, **how** to prepare them, or **who** to contact locally. 

    The **Generosity & Empathy Matchmaker** is designed to eliminate this friction entirely, merging modern AI workflows with decentralized tools to scale human kindness effortlessly.

    #### 🛠️ Technology Stack & Architecture:
    * **Google Gemini AI (`gemini-2.5-flash`):** Powers intelligent contextual categorization, preparation instructions, and custom outreach message generation.
    * **ElevenLabs API:** Delivers realistic text-to-speech voice guides for accessibility and ease of use.
    * **Solana Blockchain:** Facilitates lightning-fast, ultra-low fee cryptocurrency micro-donations with embedded QR code scanning.
    * **Snowflake Data Warehouse:** Securely captures and logs engagement telemetry data for every interaction in real-time.
    """)
    st.markdown('</div>', unsafe_allow_html=True)

# Global Persistent Footer
st.markdown("""
    <div class="footer">
        🌟 Generosity & Empathy Matchmaker • Powered by Google Gemini AI, ElevenLabs, Solana & Snowflake • Cultivating Global Kindness.
    </div>
""", unsafe_allow_html=True)
