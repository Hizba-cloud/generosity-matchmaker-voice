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
        # Ensure table exists
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS generosity_logs (
                timestamp TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
                user_contribution STRING,
                charity_category STRING
            )
        """)
        # Insert log
        cursor.execute(
            "INSERT INTO generosity_logs (user_contribution, charity_category) VALUES (%s, %s)",
            (user_input, category)
        )
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Snowflake Logging Info: {e}")

# App Page Configuration & Professional Styling
st.set_page_config(
    page_title="Generosity Matchmaker", 
    page_icon="🌟", 
    layout="centered"
)

# Custom CSS for polished aesthetics
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #FF4B4B;
        font-weight: 700;
        margin-bottom: 0px;
    }
    .sub-title {
        font-size: 1.1rem;
        color: #6c757d;
        margin-bottom: 25px;
    }
    .stButton button {
        border-radius: 8px;
        font-weight: 600;
    }
    .card {
        padding: 20px;
        border-radius: 10px;
        background-color: #f8f9fa;
        border: 1px solid #e9ecef;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# App Header Section
st.markdown('<p class="main-header">🌟 Generosity Matchmaker</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Powered by Google Gemini AI, ElevenLabs, Solana & Snowflake</p>', unsafe_allow_html=True)

with st.container():
    st.info("💡 **How it works:** Want to give back, donate items, or share your time, but aren't sure where to start? Tell us what you have or want to do, and our AI matchmaker will build a customized action plan for you!")

# User Input Form inside an aesthetic container
with st.form("match_form"):
    st.markdown("### 📝 Tell Us What You Want to Share")
    user_input = st.text_area(
        "Contribution Details",
        placeholder="e.g., I have 5 old winter jackets and some children's books, or I want to volunteer 2 hours teaching kids.",
        label_visibility="collapsed"
    )
    submit_button = st.form_submit_button("Find Match & Generate Guide ✨", use_container_width=True)

# Handle Submission & API Call
if submit_button:
    if not user_input.strip():
        st.warning("⚠️ Please enter what you'd like to contribute first!")
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
    
    # Action Plan Card Container
    with st.container():
        st.markdown("### 📋 Your Personalized Generosity Action Plan")
        st.markdown(st.session_state["match_result"])

    st.markdown("---")
    
    # Audio Guide Section
    col_audio_desc, col_audio_btn = st.columns([2, 1])
    with col_audio_desc:
        st.markdown("### 🎙️ Listen to Your Audio Guide")
        st.write("Prefer listening? Have your tailored action plan read aloud via ElevenLabs voice synthesis.")
    
    with col_audio_btn:
        generate_audio = st.button("🔊 Play Voice Guide", use_container_width=True)

    if generate_audio:
        with st.spinner("Synthesizing voice audio..."):
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
                st.success("Audio guide ready!")

            except Exception as e:
                if "402" in str(e) or "paid_plan_required" in str(e):
                    st.warning("⚠️ **ElevenLabs Free Tier Notice:** ElevenLabs free API accounts restrict the programmatic use of certain library voices. Please upgrade your ElevenLabs plan or use a compatible voice ID to enable audio playback.")
                else:
                    st.error(f"ElevenLabs Error: {e}")

    # Solana Micro-Donation Integration Section with QR Code Card
    st.markdown("---")
    st.markdown("### 🪙 Support Community Drives via Solana")
    st.write("Want to support the initiative directly? Solana enables lightning-fast, ultra-low-fee transfers so 100% of your crypto micro-contribution reaches community projects.")
    
    wallet_address = "GenerosityFundSolanaWallet11111111111111"
    
    col_qr_text, col_qr_img = st.columns([1, 1])
    with col_qr_text:
        st.markdown("**Deposit Wallet Address:**")
        st.code(wallet_address, language="text")
        st.caption("Scan the QR code with Phantom or Solflare, or copy the address to send SOL/USDC micro-donations securely.")

    with col_qr_img:
        try:
            qr = qrcode.QRCode(version=1, box_size=8, border=2)
            qr.add_data(wallet_address)
            qr.make(fit=True)
            
            img = qr.make_image(fill_color="black", back_color="white")
            buffered = BytesIO()
            img.save(buffered, format="PNG")
            
            st.image(buffered.getvalue(), width=200, caption="Scan to Donate via Solana")
        except Exception as e:
            st.caption("QR Code generation available.")
