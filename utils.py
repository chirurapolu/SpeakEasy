import soundfile as sf
import numpy as np
import streamlit as st

LANGUAGES = {
    "Arabic": "ar-SA",
    "Bengali": "bn-IN",
    "Chinese": "zh-CN",
    "Dutch": "nl-NL",
    "English": "en-US",
    "French": "fr-FR",
    "German": "de-DE",
    "Gujarati": "gu-IN",
    "Hebrew": "he-IL",
    "Hindi": "hi-IN",
    "Indonesian": "id-ID",
    "Italian": "it-IT",
    "Japanese": "ja-JP",
    "Kannada": "kn-IN",
    "Korean": "ko-KR",
    "Malayalam": "ml-IN",
    "Marathi": "mr-IN",
    "Polish": "pl-PL",
    "Portuguese": "pt-PT",
    "Punjabi": "pa-IN",
    "Russian": "ru-RU",
    "Spanish": "es-ES",
    "Swahili": "sw-KE",
    "Tamil": "ta-IN",
    "Telugu": "te-IN",
    "Thai": "th-TH",
    "Turkish": "tr-TR",
    "Urdu": "ur-PK",
    "Vietnamese": "vi-VN"
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