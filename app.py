import os
import streamlit as st
from google import genai
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
import qrcode
from io import BytesIO

# Load environment variables
load_dotenv()

# Initialize Gemini Client and ElevenLabs Client securely
client = genai.Client()
eleven_client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))

# App Styling & Layout
st.set_page_config(
    page_title="Generosity Matchmaker", 
    page_icon="🌟", 
    layout="centered"
)

st.title("🌟 Generosity Matchmaker")
st.markdown("### Powered by Google Gemini AI & ElevenLabs Voice")
st.write("Want to give back, donate items, or share your time, but aren't sure where to start? Tell us what you have or want to do, and our AI matchmaker will guide you!")

# User Input Form
with st.form("match_form"):
    user_input = st.text_area(
        "What would you like to donate or contribute?",
        placeholder="e.g., I have 5 old winter jackets and some children's books, or I want to volunteer 2 hours teaching kids."
    )
    submit_button = st.form_submit_button("Find Match & Generate Guide ✨")

# Handle Submission & API Call
if submit_button:
    if not user_input.strip():
        st.warning("Please enter what you'd like to contribute first!")
    else:
        with st.spinner("Consulting Gemini AI to find the best match..."):
            try:
                # Upgraded prompt including suggested platforms & search terms
                prompt = f"""
                You are an AI assistant for a charity and community generosity platform. 
                A user wants to give back and has provided this input: "{user_input}"
                
                Please respond with:
                1. **Recommended Category of Charity/Cause:** (e.g., Education, Warmth/Clothing Drive, Food Security)
                2. **How to Prepare Items/Time:** (3 brief bullet points on what the user should do next)
                3. **Suggested Platforms or Search Terms:** (Provide 2-3 types of verified organizations, platforms, or search queries they can use to find active drives or direct donation links nearby)
                4. **Drafted Outreach Message:** (A short, polite message the user can copy-paste to a local shelter, NGO, or community center)
                """

                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt,
                )
                
                # Save response text in session state
                st.session_state["match_result"] = response.text
                st.session_state["input_given"] = user_input

                st.success("Match found successfully!")

            except Exception as e:
                st.error(f"An error occurred with Gemini: {e}")

# Display Results & ElevenLabs Audio Feature if results exist
if "match_result" in st.session_state:
    st.markdown("### 📋 Your Generosity Action Plan")
    st.markdown(st.session_state["match_result"])

    st.markdown("---")
    st.markdown("### 🎙️ Listen to Your Audio Guide")
    st.write("Click below to hear your tailored generosity guide read aloud using ElevenLabs AI voice synthesis.")

    if st.button("🔊 Generate & Play Voice Guide"):
        with st.spinner("Synthesizing voice audio with ElevenLabs..."):
            try:
                tts_script = (
                    "Here is your personalized generosity match guide. "
                    f"Based on your contribution of: {st.session_state['input_given']}. "
                    f"Here is the plan: {st.session_state['match_result']}"
                )

                # Generate audio stream using ElevenLabs text_to_speech convert API
                audio_stream = eleven_client.text_to_speech.convert(
                    text=tts_script,
                    voice_id="21m00Tcm4TlvDq8ikWAM",
                    model_id="eleven_multilingual_v2",
                    output_format="mp3_44100_128",
                )
                
                # Consume generator into bytes
                audio_bytes = b"".join(list(audio_stream))
                
                # Play audio in Streamlit
                st.audio(audio_bytes, format="audio/mp3")
                st.success("Audio guide ready!")

            except Exception as e:
                st.error(f"ElevenLabs Error: {e}")

    # Solana Micro-Donation Integration Section with QR Code
    st.markdown("---")
    st.markdown("### 🪙 Support Community Drives via Solana")
    st.write("Prefer to support the cause with crypto micro-donations? Solana enables lightning-fast, ultra-low-fee transfers so 100% of your contribution reaches the initiative.")
    
    wallet_address = "GenerosityFundSolanaWallet11111111111111"
    st.code(wallet_address, language="text")
    
    try:
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(wallet_address)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image(buffered.getvalue(), caption="Scan with Phantom or Solflare Wallet", width=250)
            
    except Exception as e:
        st.caption("Copy the address above to send SOL or USDC micro-donations via your wallet.")
