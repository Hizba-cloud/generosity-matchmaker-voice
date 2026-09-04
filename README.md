# 🌟 Generosity Matchmaker

> An AI-powered community giving and charity companion built for the **DEV Weekend Challenge: Generosity Edition**.

## 🚀 About The Project

The **Generosity Matchmaker** is a lightweight, interactive web application designed to bridge the gap between people wanting to give back (donating items, books, clothes, or volunteer time) and local charities or community organizations. Instead of wondering how or where to contribute, users input what they have or want to do, and the app instantly generates a custom action plan—complete with a voice narration guide.

---

## 🛠️ Built With

- **Python**
- **Streamlit** (for the frontend user interface)
- **Google GenAI SDK (`gemini-2.5-flash`)** (for fast, structured natural language generation)
- **ElevenLabs API** (for accessible, human-like voice synthesis and audio guides)
- **Python-Dotenv** (for secure environment configuration)

---

## 💡 How It Works

1. **User Input:** The user types what they would like to contribute (e.g., _"I have 3 boxes of English storybooks to give away"_).
2. **Google AI Processing:** The input is sent via the Google GenAI SDK to the `gemini-2.5-flash` model.
3. **Actionable Output & Voice Guide:** Gemini analyzes the intent and dynamically returns:
   - **Recommended Category of Charity/Cause** (e.g., Education & Literacy)
   - **How to Prepare Items/Time** (Clear, practical sorting and packing checklists)
   - **Drafted Outreach Message** (A polite, ready-to-copy template for local shelters or NGOs)
4. **ElevenLabs Narration:** Users can click to listen to their entire action plan read aloud via ElevenLabs text-to-speech for seamless accessibility.

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
```
