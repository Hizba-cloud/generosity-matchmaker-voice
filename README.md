# 🌟 Generosity Matchmaker

> An AI-powered community giving and charity companion built for the **DEV Weekend Challenge: Generosity Edition**.

## 🚀 About The Project

The **Generosity Matchmaker** is a lightweight, interactive web application designed to bridge the gap between people wanting to give back (donating items, books, clothes, or volunteer time) and local charities or community organizations. Instead of wondering how or where to contribute, users input what they have or want to do, and the app instantly generates a custom action plan—complete with verified platform search terms, an audio voice narration guide, and lightning-fast Solana micro-donations.

---

## 🛠️ Built With

- **Python**
- **Streamlit** (for the frontend user interface)
- **Google GenAI SDK (`gemini-2.5-flash`)** (for fast, structured natural language generation)
- **ElevenLabs API** (for accessible, human-like voice synthesis and audio guides)
- **Solana & Python-QRcode** (for instant, low-fee web3 micro-donations via scannable QR codes)
- **Python-Dotenv** (for secure environment configuration)

---

## 💡 How It Works

1. **User Input:** The user types what they would like to contribute (e.g., _"I have 3 boxes of English storybooks to give away"_).
2. **Google AI Processing:** The input is sent via the Google GenAI SDK to the `gemini-2.5-flash` model using an enhanced system prompt.
3. **Actionable Output & Voice Guide:** Gemini analyzes the intent and dynamically returns:
   - **Recommended Category of Charity/Cause** (e.g., Education & Literacy)
   - **How to Prepare Items/Time** (Clear, practical sorting and packing checklists)
   - **Suggested Platforms or Search Terms** (Verified organizations, platforms, or search queries to find active drives and direct donation links nearby)
   - **Drafted Outreach Message** (A polite, ready-to-copy template for local shelters or NGOs)
4. **ElevenLabs Narration:** Users can click to listen to their entire action plan read aloud via ElevenLabs text-to-speech for seamless accessibility.
5. **Solana Micro-Donations:** Users can instantly support community initiatives with low-fee ($0.00025) crypto contributions by scanning the automatically generated Solana QR code with a wallet like Phantom or Solflare.

---

## 📂 Project Structure

```text
generosity-matchmaker/
│
├── app.py              # Main Streamlit web application
├── requirements.txt    # Project dependencies
├── .env                # Local environment variables (API keys - ignored by git)
├── .gitignore          # Git exclusion rules
└── README.md           # Project documentation
