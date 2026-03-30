import streamlit as st
import edge_tts
import asyncio
import tempfile
import os
from io import BytesIO
import time
from utils import LANGUAGES
from gtts import gTTS

async def get_valid_voice(lang_code, gender):
    voices = await edge_tts.list_voices()
    target_gender = "Female" if gender == "Female" else "Male"
    # match locale exactly
    for v in voices:
        if v["Locale"] == lang_code and v["Gender"] == target_gender:
            return v["ShortName"]
    # match locale language only
    lang_prefix = lang_code.split('-')[0]
    for v in voices:
        if v["Locale"].startswith(lang_prefix) and v["Gender"] == target_gender:
            return v["ShortName"]
    # fallback
    return "en-US-AriaNeural" if target_gender == "Female" else "en-US-ChristopherNeural"

async def _generate_audio_bytes(text, lang_code, gender, rate_str):
    voice = await get_valid_voice(lang_code, gender)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        temp_path = fp.name
    communicate = edge_tts.Communicate(text, voice, rate=rate_str)
    await communicate.save(temp_path)
    with open(temp_path, "rb") as f:
        data = f.read()
    os.unlink(temp_path)
    return data

def text_to_speech_tab():
    st.markdown("""
    <div class="tab-content" id="text-to-speech-content">
        <h2 class="section-title">Speech Synthesis (High Quality Neural Voices)</h2>
        <p style='color: gray; font-size: 0.9em; margin-top: -10px; margin-bottom: 25px;'>Powered by Microsoft Edge TTS - Features Siri/Gemini level clarity</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        tts_lang = st.selectbox(
            "Select output language:",
            options=list(LANGUAGES.keys()),
            index=list(LANGUAGES.keys()).index("English") if "English" in LANGUAGES else 0,
            key="tts_lang"
        )

        voice_gender = st.radio(
            "Voice gender:",
            ("Male", "Female"),
            horizontal=True,
            key="voice_gender"
        )

        voice_speed = st.slider(
            "Speech rate (WPM equivalent):",
            100, 300, 175,
            key="voice_speed"
        )

    with col2:
        text_input = st.text_area(
            "Enter text to convert to speech:",
            height=200,
            key="tts_text",
            placeholder="Type or paste your text here..."
        )

        btn_col1, btn_col2 = st.columns([1, 1])

        # edge-tts rate conversion (+xx% or -xx%)
        rate_pct = int((voice_speed - 175) / 175 * 100)
        rate_str = f"+{rate_pct}%" if rate_pct >= 0 else f"{rate_pct}%"

        with btn_col1:
            if st.button("▶️ Play Speech", key="play_speech"):
                if text_input:
                    with st.spinner("Generating High-Quality Neural Audio..."):
                        try:
                            lang_code = LANGUAGES.get(tts_lang, "en-US")
                            audio_bytes = asyncio.run(_generate_audio_bytes(text_input, lang_code, voice_gender, rate_str))
                            st.audio(audio_bytes, format="audio/mpeg", autoplay=True)
                            st.success("Playback started!")
                        except Exception as e:
                            if "No audio was received" in str(e) or "WebSocket" in str(e):
                                st.warning("⚠️ High-quality voice unsupported for this text/language. Falling back to standard Google TTS...")
                                try:
                                    short_lang = lang_code.split('-')[0]
                                    tts = gTTS(text=text_input, lang=short_lang)
                                    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                                        temp_path = fp.name
                                    tts.save(temp_path)
                                    with open(temp_path, "rb") as f:
                                        fallback_audio = f.read()
                                    os.unlink(temp_path)
                                    st.audio(fallback_audio, format="audio/mpeg", autoplay=True)
                                    st.success("Playback started (Google TTS)!")
                                except Exception as fallback_e:
                                    st.error(f"❌ Both TTS engines failed. Fallback error: {fallback_e}")
                            else:
                                st.error(f"❌ Error generating speech: {e}")
                else:
                    st.warning("⚠️ Please enter some text first")

        with btn_col2:
            if st.button("📥 Download Audio", key="download_audio"):
                if text_input:
                    with st.spinner("Generating High-Quality Audio file..."):
                        try:
                            lang_code = LANGUAGES.get(tts_lang, "en-US")
                            audio_bytes = asyncio.run(_generate_audio_bytes(text_input, lang_code, voice_gender, rate_str))
                            st.success("Audio ready for download!")
                            st.download_button(
                                label="💾 Download MP3",
                                data=audio_bytes,
                                file_name="high_quality_speech.mp3",
                                mime="audio/mpeg",
                                key="final_download"
                            )
                        except Exception as e:
                            if "No audio was received" in str(e) or "WebSocket" in str(e):
                                st.warning("⚠️ High-quality voice unsupported for this text/language. Falling back to standard Google TTS...")
                                try:
                                    short_lang = lang_code.split('-')[0]
                                    tts = gTTS(text=text_input, lang=short_lang)
                                    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                                        temp_path = fp.name
                                    tts.save(temp_path)
                                    with open(temp_path, "rb") as f:
                                        fallback_audio = f.read()
                                    os.unlink(temp_path)
                                    st.download_button(
                                        label="💾 Download Fallback MP3",
                                        data=fallback_audio,
                                        file_name="standard_speech.mp3",
                                        mime="audio/mpeg",
                                        key="fallback_download"
                                    )
                                except Exception as fallback_e:
                                    st.error(f"❌ Both TTS engines failed. Fallback error: {fallback_e}")
                            else:
                                st.error(f"❌ Error generating speech: {e}")
                else:
                    st.warning("⚠️ Please enter some text first")