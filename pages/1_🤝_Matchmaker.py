import os
import streamlit as st
from google import genai
from elevenlabs.client import ElevenLabs
import qrcode
from io import BytesIO
import snowflake.connector

client = genai.Client()
eleven_client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))

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

st.markdown('<p class="main-header">🤝 Generosity Matchmaker</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Connect your resources, skills, and time directly with verified community causes.</p>', unsafe_allow_html=True)

col_main, col_side = st.columns([2, 1], gap="large")

with col_main:
    st.markdown('<div class="card-box">', unsafe_allow_html=True)
    st.markdown("### 📝 Share Your Contribution")
    st.info("💡 Select a quick-action cause below or type your custom offering to generate an instant action plan.")

    if "input_text" not in st.session_state:
        st.session_state["input_text"] = ""

    st.markdown("**Quick-Select Causes:**")
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
            placeholder="e.g., I want to donate clean clothes or offer tutoring time...",
            height=120
        )
        submit_button = st.form_submit_button("Generate AI Impact Roadmap ✨", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_side:
    st.markdown('<div class="card-box">', unsafe_allow_html=True)
    st.markdown("### 🌍 Empathy in Action")
    st.image(
        "https://images.unsplash.com/photo-1593113598332-cd288d649433?auto=format&fit=crop&w=600&q=80",
        use_container_width=True,
        caption="Bridging hearts and communities."
    )
    st.markdown("""
    * **Tailored Guidance:** Powered by Gemini AI.
    * **Voice Enabled:** Accessible audio guides.
    * **Decentralized Support:** Lightning-fast Solana micro-donations.
    """)
    st.markdown('</div>', unsafe_allow_html=True)

if submit_button:
    if not user_input.strip():
        st.warning("⚠️ Please enter or select what you'd like to contribute first!")
    else:
        with st.spinner("✨ Consulting Gemini AI to map your community impact..."):
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

if "match_result" in st.session_state:
    st.markdown("---")
    res_col1, res_col2 = st.columns(2, gap="large")
    
    with res_col1:
        st.markdown('<div class="card-box">', unsafe_allow_html=True)
        st.markdown("### 📋 Your Tailored Action Plan")
        st.markdown(st.session_state["match_result"])
        st.markdown('</div>', unsafe_allow_html=True)

    with res_col2:
        st.markdown('<div class="card-box">', unsafe_allow_html=True)
        st.markdown("### 🎙️ Audio Accessibility Guide")
        st.write("Listen to your impact roadmap read aloud via ElevenLabs voice synthesis.")
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
                    st.success("Audio guide ready!")
                except Exception as e:
                    st.error(f"ElevenLabs Error: {e}")

        st.markdown("---")
        st.markdown("### 🪙 Community Support via Solana")
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
