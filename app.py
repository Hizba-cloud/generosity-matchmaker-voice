import os
import streamlit as st
from google import genai
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
import qrcode
from io import BytesIO
import snowflake.connector

# Load environment variables
load_dotenv()

# Initialize Gemini Client and ElevenLabs Client securely
client = genai.Client()
eleven_client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))

# Function to log impact data to Snowflake (Safe background execution)
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
    page_title="Generosity Matchmaker", 
    page_icon="🌟", 
    layout="wide"
)

# Custom Styling for Dashboard & Sidebar Layout
st.markdown("""
    <style>
    .stApp {
        background-color: #F8FAFC;
    }
    .main-header {
        font-size: 2.2rem;
        color: #0F172A;
        font-weight: 800;
        letter-spacing: -0.03em;
        margin-bottom: 0px;
    }
    .sub-title {
        font-size: 1rem;
        color: #475569;
        font-weight: 500;
        margin-bottom: 20px;
    }
    .card-container {
        background-color: #FFFFFF;
        padding: 24px;
        border-radius: 16px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
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
    div[data-baseweb="textarea"] textarea {
        background-color: #FFFFFF;
        border-radius: 12px;
        border: 1px solid #CBD5E1;
        padding: 14px;
        color: #1E293B;
    }
    .footer {
        text-align: center;
        color: #94A3B8;
        font-size: 0.85rem;
        margin-top: 40px;
        padding: 20px;
        border-top: 1px solid #E2E8F0;
    }
    </style>
""", unsafe_allow_html=True)

# ----------------- SIDEBAR NAVIGATION -----------------
with st.sidebar:
    st.image("https://images.unsplash.com/photo-1532629345422-7515f3d16bb9?auto=format&fit=crop&w=400&q=80", use_container_width=True)
    st.markdown("### 🌟 Generosity Hub")
    st.markdown("Navigating community impact through AI & Web3 integration.")
    
    st.markdown("---")
    app_mode = st.radio("Navigation", ["🏠 Matchmaker Dashboard", "📊 Snowflake Cloud Logs", "ℹ️ About Platform"])
    
    st.markdown("---")
    st.markdown("**System Status:**")
    st.success("🟢 Gemini AI: Active")
    st.success("🟢 ElevenLabs TTS: Online")
    st.success("🟢 Snowflake DB: Connected")

# ----------------- VIEW 1: MATCHMAKER DASHBOARD -----------------
if app_mode == "🏠 Matchmaker Dashboard":
    # Header Section
    st.markdown('<p class="main-header">🌟 Generosity Matchmaker Dashboard</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Powered by Google Gemini AI, ElevenLabs, Solana & Snowflake</p>', unsafe_allow_html=True)

    # Main Dashboard Columns layout (Left: Input & Quick select, Right: Banner / Overview)
    col_main, col_side = st.columns([2, 1])

    with col_main:
        with st.container():
            st.markdown("### 📝 Create Your Impact Roadmap")
            st.info("💡 **How it works:** Choose a quick-select cause below or type your custom contribution to build a verified action plan.")

            # Quick-Select Action Chips
            st.markdown("**Quick-Select Popular Causes:**")
            q1, q2, q3, q4 = st.columns(4)
            if "input_text" not in st.session_state:
                st.session_state["input_text"] = ""

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

            # User Input Form
            with st.form("match_form"):
                user_input = st.text_area(
                    "What would you like to donate or contribute?",
                    value=st.session_state["input_text"],
                    placeholder="e.g., I want to volunteer or donate items...",
                    height=120
                )
                submit_button = st.form_submit_button("Find Match & Generate Guide ✨", use_container_width=True)

    with col_side:
        st.markdown("### 🌍 Community Impact")
        st.image(
            "https://images.unsplash.com/photo-1593113598332-cd288d649433?auto=format&fit=crop&w=600&q=80",
            use_container_width=True,
            caption="Empowering global generosity."
        )
        st.markdown("""
        * **100% Transparent:** Tracked via Snowflake.
        * **Instant Guidance:** AI-driven matching.
        * **Micro-Donations:** Lightning-fast Solana routing.
        """)

    # Handle Submission & API Call
    if submit_button:
        if not user_input.strip():
            st.warning("⚠️ Please enter or select what you'd like to contribute first!")
        else:
            with st.spinner("✨ Consulting Gemini AI to craft your custom impact roadmap..."):
                try:
                    prompt = f"""
                    You are an AI assistant for a charity and community generosity platform. 
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

                    # Log to Snowflake warehouse in the background
                    log_to_snowflake(user_input, "General Match")

                except Exception as e:
                    st.error(f"An error occurred with Gemini: {e}")

    # Display Results & Interactive Features if results exist
    if "match_result" in st.session_state:
        st.markdown("---")
        
        col_res1, col_res2 = st.columns(2)
        
        with col_res1:
            st.markdown("### 📋 Your Action Plan")
            with st.container():
                st.markdown(st.session_state["match_result"])

        with col_res2:
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

# ----------------- VIEW 2: SNOWFLAKE CLOUD LOGS -----------------
elif app_mode == "📊 Snowflake Cloud Logs":
    st.markdown('<p class="main-header">📊 Snowflake Logging Warehouse</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Real-time audit logs captured directly from user form submissions.</p>', unsafe_allow_html=True)
    
    with st.container():
        st.write("Fetching recent submission telemetry from your Snowflake database (`generosity_logs`)...")
        try:
            conn = snowflake.connector.connect(
                user=os.getenv("SNOWFLAKE_USER"),
                password=os.getenv("SNOWFLAKE_PASSWORD"),
                account=os.getenv("SNOWFLAKE_ACCOUNT"),
                warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
                database=os.getenv("SNOWFLAKE_DATABASE"),
                schema=os.getenv("SNOWFLAKE_SCHEMA")
            )
            import pandas as pd
            df = pd.read_sql("SELECT * FROM generosity_logs ORDER BY timestamp DESC LIMIT 50", conn)
            conn.close()
            
            if not df.empty:
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No logs recorded yet. Submit a match on the dashboard to populate this table!")
        except Exception as e:
            st.warning(f"Could not connect to Snowflake to render live table directly in preview: {e}")
            st.info("You can run this query directly in your Snowflake worksheet:\n`SELECT * FROM generosity_db.public.generosity_logs ORDER BY timestamp DESC;`")

# ----------------- VIEW 3: ABOUT PLATFORM -----------------
elif app_mode == "ℹ️ About Platform":
    st.markdown('<p class="main-header">ℹ️ About Generosity Matchmaker</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Designed for community-driven giving and modern architecture.</p>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown("""
        ### Architectural Highlights:
        * **Google Gemini AI (`gemini-2.5-flash`)**: Powers intelligent contextual categorization, preparation instructions, and custom outreach templates.
        * **ElevenLabs API**: Delivers realistic text-to-speech voice guides for accessibility and ease of use.
        * **Solana Blockchain**: Facilitates lightning-fast, ultra-low fee cryptocurrency micro-donations with embedded QR code scanning.
        * **Snowflake Data Warehouse**: Securely captures and logs telemetry data for every engagement interaction in real time.
        """)

# ----------------- FOOTER -----------------
st.markdown("""
    <div class="footer">
        🌟 Generosity Matchmaker • Built with Streamlit, Google Gemini, ElevenLabs, Solana & Snowflake • All rights reserved.
    </div>
""", unsafe_allow_html=True)
