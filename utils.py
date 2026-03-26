import soundfile as sf
import numpy as np
import streamlit as st

LANGUAGES = {
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

def convert_to_wav(input_file, output_path):
    try:
        data, samplerate = sf.read(input_file)
        if len(data.shape) > 1:
            data = np.mean(data, axis=1)
        if data.dtype == np.float32 or data.dtype == np.float64:
            data = (data * 32767).astype(np.int16)
        sf.write(output_path, data, samplerate, subtype='PCM_16')
        return True
    except Exception as e:
        st.error(f"Error converting audio: {e}")
        return False