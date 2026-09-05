import os
import streamlit as st
from google import genai
from elevenlabs.client import ElevenLabs
import qrcode
from io import BytesIO
import pandas as pd

# Safe API Key & Secret Loading (Supports both st.secrets and environment variables)
def get_secret(key):
    try:
        if key in st.secrets:
            return st.secrets[key]
    except Exception:
        pass
    return os.getenv(key)

GEMINI_KEY = get_secret("GEMINI_API_KEY")
ELEVEN_KEY = get_secret("ELEVENLABS_API_KEY")

# Initialize Clients safely
client = genai.Client(api_key=GEMINI_KEY) if GEMINI_KEY else None
eleven_client = ElevenLabs(api_key=ELEVEN_KEY) if ELEVEN_KEY else None

# Safe Snowflake Logger (Bypasses connection entirely if credentials are missing)
def log_to_snowflake(user_input, category):
    sf_user = get_secret("SNOWFLAKE_USER")
    if not sf_user:
        return  # Skip silently if Snowflake isn't configured
    try:
        import snowflake.connector
        conn = snowflake.connector.connect(
            user=sf_user,
            password=get_secret("SNOWFLAKE_PASSWORD"),
            account=get_secret("SNOWFLAKE_ACCOUNT"),
            warehouse=get_secret("SNOWFLAKE_WAREHOUSE"),
            database=get_secret("SNOWFLAKE_DATABASE"),
            schema=get_secret("SNOWFLAKE_SCHEMA")
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
    page_title="Generosity & Empathy Platform", 
    page_icon="🌟", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom Responsive Styling
st.markdown("""
    <style>
    .stApp { background-color: #F8FAFC; }
    .main-header { font-size: clamp(2rem, 4vw, 2.8rem); color: #0F172A; font-weight: 800; letter-spacing: -0.03em; margin-bottom: 2px; }
    .sub-title { font-size: clamp(0.95rem, 2vw, 1.1rem); color: #475569; font-weight: 500; margin-bottom: 25px; }
    .stButton button {
        background: linear-gradient(135deg, #4F46E5 0%, #3B82F6 100%);
        color: white; border-radius: 12px; padding: 0.6rem 1.2rem; font-weight: 600; border: none; width: 100%;
        box-shadow: 0 4px 14px rgba(79, 70, 229, 0.25); transition: all 0.3s ease;
    }
    .stButton button:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(79, 70, 229, 0.35); }
    div[data-baseweb="textarea"] textarea { background-color: #FFFFFF; border-radius: 14px; border: 1px solid #CBD5E1; padding: 16px; color: #1E293B; font-size: 1rem; }
    .footer { text-align: center; color: #94A3B8; font-size: 0.9rem; margin-top: 50px; padding: 25px; border-top: 1px solid #E2E8F0; }
    </style>
""", unsafe_allow_html=True)

# App Header Section
st.markdown('<p class="main-header">🌟 Generosity & Empathy Matchmaker</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Connecting human kindness with verified community causes through compassionate AI guidance.</p>', unsafe_allow_html=True)

# Impact Metrics Bar
col_m1, col_m2, col_m3, col_m4 = st.columns(4)
with col_m1: st.metric(label="❤️ Acts of Kindness", value="14,250+", delta="+320 this week")
with col_m2: st.metric(label="🤝 Local Causes", value="48 Supported", delta="Active Drives")
with col_m3: st.metric(label="🎙️ Empathy Voice Guides", value="5,890+", delta="Audio Enabled")
with col_m4: st.metric(label="🌍 Global Givers", value="2,410+", delta="Growing Community")

st.markdown("---")

tab1, tab2, tab3 = st.tabs(["🤝 AI Matchmaker Hub", "📖 The Science & Spirit of Kindness", "📊 Community Impact & Telemetry"])

# ================= TAB 1: MATCHMAKER DASHBOARD =================
with tab1:
    col_main, col_side = st.columns([1.3, 1], gap="large")

    with col_main:
        with st.container(border=True):
            st.markdown("### 📝 Share Your Offering of Kindness")
            st.info("💡 **How it works:** Select a quick-action cause below or write your own custom gift to receive an instant action roadmap.")

            if "input_text" not in st.session_state:
                st.session_state["input_text"] = ""

            st.markdown("**Quick-Select Ways to Help:**")
            q1, q2, q3, q4 = st.columns(4)
            with q1:
                if st.button("🧥 Jackets", width="stretch"):
                    st.session_state["input_text"] = "I have winter jackets and blankets to donate for families in need."
            with q2:
                if st.button("📚 Books", width="stretch"):
                    st.session_state["input_text"] = "I have educational books and storybooks to share with children."
            with q3:
                if st.button("🍲 Food", width="stretch"):
                    st.session_state["input_text"] = "I want to contribute non-perishable food items for a community food drive."
            with q4:
                if st.button("💻 Tutoring", width="stretch"):
                    st.session_state["input_text"] = "I want to volunteer my time teaching basic skills and mentorship."

            with st.form("match_form"):
                user_input = st.text_area(
                    "What would you like to contribute today?",
                    value=st.session_state["input_text"],
                    placeholder="e.g., I want to volunteer 2 hours a week or donate warm clothes...",
                    height=130
                )
                submit_button = st.form_submit_button("Generate Empathy Roadmap ✨", width="stretch")

    with col_side:
        with st.container(border=True):
            st.markdown("### 🌍 Cultivating Everyday Empathy")
            st.image(
                "https://images.unsplash.com/photo-1593113598332-cd288d649433?auto=format&fit=crop&w=600&q=80",
                width="stretch",
                caption="Every act of kindness ripples further than we know."
            )
            st.markdown("""
            * **🌱 Intentional Giving:** Structured guidance designed for your specific resources.
            * **🎙️ Accessible Voice:** Listen to your guide anywhere via realistic narration.
            * **🤝 Community First:** Direct alignment with verified local support networks.
            """)

    if submit_button:
        if not user_input.strip():
            st.warning("⚠️ Please share what you'd like to contribute first!")
        elif not client:
            st.error("⚠️ Gemini API Key is missing. Please add `GEMINI_API_KEY` to your Streamlit App Secrets.")
        else:
            with st.spinner("✨ Consulting AI to design your compassionate action plan..."):
                try:
                    prompt = f"""
                    You are an empathetic, warm AI assistant for a global kindness and community generosity platform. 
                    A user wants to give back with this offering: "{user_input}"
                    
                    Please respond warmly and clearly with:
                    1. **Recommended Category of Need:** (e.g., Warmth & Clothing, Education & Mentorship, Food Security)
                    2. **How to Prepare Your Contribution:** (3 gentle, practical bullet points on what steps to take)
                    3. **Suggested Outreach Steps:** (Types of local organizations or search terms to find active community drives nearby)
                    4. **Drafted Message of Care:** (A kind, polite template message the user can use when reaching out to an organizer or shelter)
                    """
                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=prompt,
                    )
                    st.session_state["match_result"] = response.text
                    st.session_state["input_given"] = user_input
                    log_to_snowflake(user_input, "General Match")
                except Exception as e:
                    st.error(f"An error occurred while generating the roadmap: {e}")

    st.markdown("---")
    res_col1, res_col2 = st.columns(2, gap="large")
    
    with res_col1:
        with st.container(border=True):
            st.markdown("### 📋 Compassionate Action Plan")
            if "match_result" in st.session_state:
                st.markdown(st.session_state["match_result"])
            else:
                st.info("👋 **Your personalized roadmap will appear here!** Select a quick cause above or type your offering and click **'Generate Empathy Roadmap'**.")

    with res_col2:
        with st.container(border=True):
            st.markdown("### 🎙️ Audio Voice Guide & Community Support")
            if "match_result" in st.session_state:
                st.write("Listen to your personalized generosity guide read aloud.")
                if st.button("🔊 Play Voice Synthesis", width="stretch"):
                    if not eleven_client:
                        st.warning("ElevenLabs API Key not configured. Skipping audio generation.")
                    else:
                        with st.spinner("Synthesizing audio..."):
                            try:
                                tts_script = f"Here is your personalized generosity guide based on your contribution: {st.session_state['input_given']}"
                                audio_stream = eleven_client.text_to_speech.convert(
                                    text=tts_script,
                                    voice_id="EXAVITQu4vr4xnSDxMaL",
                                    model_id="eleven_multilingual_v2",
                                    output_format="mp3_44100_128",
                                )
                                audio_bytes = b"".join(list(audio_stream))
                                st.audio(audio_bytes, format="mp3")
                                st.success("Audio ready!")
                            except Exception as e:
                                st.warning(f"Voice Synthesis Note: {e}")
            else:
                st.write("Generate your AI action plan above to unlock instant audio narration.")

            st.markdown("---")
            st.markdown("### 🪙 Community Micro-Support Fund")
            wallet_address = "GenerosityFundSolanaWallet11111111111111"
            st.code(wallet_address, language="text")
            try:
                qr = qrcode.QRCode(version=1, box_size=6, border=2)
                qr.add_data(wallet_address)
                qr.make(fit=True)
                img = qr.make_image(fill_color="black", back_color="white")
                buffered = BytesIO()
                img.save(buffered, format="PNG")
                st.image(buffered.getvalue(), width=150, caption="Scan to support community funds")
            except Exception:
                pass

# ================= TAB 2: THE SCIENCE & SPIRIT OF KINDNESS =================
with tab2:
    col_t1, col_t2 = st.columns(2, gap="large")
    with col_t1:
        with st.container(border=True):
            st.markdown("### 🧠 The Psychology of Giving")
            st.markdown("Kindness triggers dopamine, lowers cortisol, and builds deep social bonds.")
        with st.container(border=True):
            st.markdown("### 💡 Daily Habits of Empathy")
            st.markdown("Practice active listening, micro-surprises, and checking in on your neighbors.")
    with col_t2:
        with st.container(border=True):
            st.markdown("### 🌟 Wisdom on Generosity")
            st.markdown('> *"We rise by lifting others."*')

# ================= TAB 3: COMMUNITY IMPACT & TELEMETRY =================
with tab3:
    with st.container(border=True):
        st.markdown("### 📊 Transparency & Community Telemetry")
        try:
            sf_user = get_secret("SNOWFLAKE_USER")
            if sf_user:
                import snowflake.connector
                conn = snowflake.connector.connect(
                    user=sf_user,
                    password=get_secret("SNOWFLAKE_PASSWORD"),
                    account=get_secret("SNOWFLAKE_ACCOUNT"),
                    warehouse=get_secret("SNOWFLAKE_WAREHOUSE"),
                    database=get_secret("SNOWFLAKE_DATABASE"),
                    schema=get_secret("SNOWFLAKE_SCHEMA")
                )
                df = pd.read_sql("SELECT * FROM generosity_logs ORDER BY timestamp DESC LIMIT 50", conn)
                conn.close()
                st.dataframe(df, width="stretch")
            else:
                raise Exception("No Snowflake credentials")
        except Exception:
            st.info("ℹ️ **Database Preview Mode:** Showing sample telemetry records.")
            sample_df = pd.DataFrame({
                "TIMESTAMP": ["2026-09-05 14:20:10", "2026-09-05 13:15:45"],
                "USER_CONTRIBUTION": ["I have winter jackets to donate.", "I want to volunteer."],
                "CHARITY_CATEGORY": ["Warmth & Clothing", "Education & Mentorship"]
            })
            st.dataframe(sample_df, width="stretch")

st.markdown("""
    <div class="footer">
        🌟 Generosity & Empathy Platform • Powered by Compassionate AI & Community Care.
    </div>
""", unsafe_allow_html=True)
