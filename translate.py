import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# Configure the Gemini API
try:
    # Remove any 'environment' parameter
    genai.configure(api_key=os.getenv("AIzaSyA68Fn2F620ByQZvM9pza37TgTuejNYS8M"))
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"❌ Error: Could not configure Gemini API. Please check your API key and environment. Error Details: {e}")

LANGUAGES = {
    "Auto Detect": "",
    "Arabic": "ar",
    "Bengali": "bn",
    "Chinese": "zh",
    "Dutch": "nl",
    "English": "en",
    "French": "fr",
    "German": "de",
    "Gujarati": "gu",
    "Hebrew": "he",
    "Hindi": "hi",
    "Indonesian": "id",
    "Italian": "it",
    "Japanese": "ja",
    "Kannada": "kn",
    "Korean": "ko",
    "Malayalam": "ml",
    "Marathi": "mr",
    "Polish": "pl",
    "Portuguese": "pt",
    "Punjabi": "pa",
    "Russian": "ru",
    "Spanish": "es",
    "Swahili": "sw",
    "Tamil": "ta",
    "Telugu": "te",
    "Thai": "th",
    "Turkish": "tr",
    "Urdu": "ur",
    "Vietnamese": "vi"
}

def translate_text_gemini(text, source_language, target_language):
    """Translates text using Gemini API"""
    try:
        prompt = f"Translate the following {source_language} text to {target_language} and provide a brief explanation: '\n{text}'"
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"❌ Translation error (Gemini): {e}"

def show_translation_ui(text, source_lang_key):
    """Handles translation UI with session state"""
    # Initialize session state for translation if not exists
    if 'show_translation' not in st.session_state:
        st.session_state.show_translation = False
    
    # Toggle translation UI when button is clicked
    if st.button("🌐 Translate to other language", key="translate_button"):
        st.session_state.show_translation = not st.session_state.show_translation
    
    # Show translation UI if toggled on
    if st.session_state.show_translation:
        target_lang_key = st.selectbox(
            "Select target language for translation:",
            options=list(LANGUAGES.keys()),
            key="target_lang_selection"
        )
        
        if target_lang_key and text:
            try:
                translation_text = translate_text_gemini(
                    text, 
                    LANGUAGES[source_lang_key], 
                    LANGUAGES[target_lang_key]
                )
                st.markdown(f"""
                <div class="result-box">
                    <p><b>Translation ({target_lang_key}):</b> {translation_text}</p>
                </div>
                """, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"❌ An error occurred during translation: {e}")