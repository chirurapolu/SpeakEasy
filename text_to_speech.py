import streamlit as st
import pyttsx3
from gtts import gTTS
from io import BytesIO
import time
import threading
from utils import LANGUAGES

def text_to_speech_tab():
    # CSS for animations
    st.markdown("""
    <style>
        @keyframes pulse {
            0% { transform: scale(1); opacity: 0.7; }
            50% { transform: scale(1.1); opacity: 1; }
            100% { transform: scale(1); opacity: 0.7; }
        }
        @keyframes glow {
            0% { filter: drop-shadow(0 0 5px #4CAF50); }
            50% { filter: drop-shadow(0 0 20px #4CAF50); }
            100% { filter: drop-shadow(0 0 5px #4CAF50); }
        }
        .fullscreen-animation {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.85);
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: column;
            z-index: 9999;
        }
        .studio-mic {
            position: relative;
            width: 200px;
            height: 300px;
            margin-bottom: 2rem;
        }
        .mic-stand {
            position: absolute;
            bottom: 0;
            left: 50%;
            transform: translateX(-50%);
            width: 20px;
            height: 150px;
            background: #555;
            border-radius: 5px;
        }
        .mic-base {
            position: absolute;
            bottom: -30px;
            left: 50%;
            transform: translateX(-50%);
            width: 100px;
            height: 20px;
            background: #333;
            border-radius: 10px;
        }
        .mic-head {
            position: absolute;
            top: 0;
            left: 50%;
            transform: translateX(-50%);
            width: 80px;
            height: 80px;
            background: #222;
            border-radius: 50%;
            animation: pulse 1.5s infinite, glow 2s infinite;
            display: flex;
            justify-content: center;
            align-items: center;
            color: white;
            font-size: 2rem;
        }
        .sound-waves {
            display: flex;
            justify-content: center;
            gap: 8px;
            height: 60px;
            align-items: flex-end;
            margin-top: 20px;
        }
        .wave {
            width: 8px;
            background: #4CAF50;
            border-radius: 4px;
            animation: wave 1.2s infinite ease-in-out;
        }
        .wave:nth-child(1) { animation-delay: 0s; height: 10px; }
        .wave:nth-child(2) { animation-delay: 0.2s; height: 30px; }
        .wave:nth-child(3) { animation-delay: 0.4s; height: 50px; }
        .wave:nth-child(4) { animation-delay: 0.6s; height: 30px; }
        .wave:nth-child(5) { animation-delay: 0.8s; height: 10px; }
        @keyframes wave {
            0%, 100% { height: 10px; }
            50% { height: 60px; }
        }
        .status-text {
            color: white;
            font-size: 1.5rem;
            margin-top: 2rem;
            text-align: center;
        }
        .online-icon {
            font-size: 5rem;
            animation: pulse 1.5s infinite;
            color: #4CAF50;
            margin-bottom: 1rem;
        }
    </style>
    """, unsafe_allow_html=True)

    # Main UI
    st.markdown("""
    <div class="tab-content" id="text-to-speech-content">
        <h2 class="section-title">Speech Synthesis</h2>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        tts_lang = st.selectbox(
            "Select output language:",
            options=list(LANGUAGES.keys()),
            index=list(LANGUAGES.keys()).index("English"),
            key="tts_lang"
        )

        voice_gender = st.radio(
            "Voice gender:",
            ("Male", "Female"),
            horizontal=True,
            key="voice_gender"
        )

        voice_speed = st.slider(
            "Speech rate:",
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

        with btn_col1:
            if st.button("▶️ Play Speech", key="play_speech"):
                if text_input:
                    # Create a placeholder for the animation
                    animation_placeholder = st.empty()
                    
                    # Show studio mic animation
                    animation_placeholder.markdown("""
                    <div class="fullscreen-animation">
                        <div class="studio-mic">
                            <div class="mic-stand"></div>
                            <div class="mic-base"></div>
                            <div class="mic-head">🎙️</div>
                        </div>
                        <div class="sound-waves">
                            <div class="wave"></div>
                            <div class="wave"></div>
                            <div class="wave"></div>
                            <div class="wave"></div>
                            <div class="wave"></div>
                        </div>
                        <div class="status-text">Recording in progress...</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    try:
                        # Function to handle speech completion
                        def on_end(name, completed):
                            # Remove animation when speech completes
                            animation_placeholder.empty()
                        
                        # Initialize engine
                        engine = pyttsx3.init()
                        engine.setProperty('rate', voice_speed)
                        voices = engine.getProperty('voices')
                        
                        # Find appropriate voice
                        target_lang_code = LANGUAGES[tts_lang].lower()
                        best_voice_id = None
                        
                        if target_lang_code == 'en':
                            if voice_gender == "Female":
                                best_voice_id = next((v.id for v in voices if "samantha" in v.name.lower()), None)
                            else:
                                best_voice_id = next((v.id for v in voices if "daniel" in v.name.lower()), None)
                        
                        if not best_voice_id:
                            matching_voices = []
                            for v in voices:
                                langs = v.languages
                                if langs and isinstance(langs, (list, tuple)) and any(target_lang_code in str(l).lower() for l in langs):
                                    matching_voices.append(v)
                            if matching_voices:
                                best_voice_id = matching_voices[0].id
                            else:
                                best_voice_id = voices[0 if voice_gender == "Male" else 1].id
                                
                        engine.setProperty('voice', best_voice_id)
                        
                        # Connect end event
                        engine.connect('finished-utterance', on_end)
                        
                        # Speak the text
                        engine.say(text_input)
                        engine.runAndWait()
                        
                        # Ensure animation is cleared even if on_end fails
                        animation_placeholder.empty()
                        
                    except Exception as e:
                        # Remove animation on error
                        animation_placeholder.empty()
                        st.error(f"❌ Error with local speech engine: {e}")
                        st.info("🔄 Falling back to online speech synthesis...")
                        
                        try:
                            # Show generating animation
                            animation_placeholder.markdown("""
                            <div class="fullscreen-animation">
                                <div class="online-icon">🌐</div>
                                <div class="status-text">Connecting to online speech synthesis service...</div>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Generate online speech
                            tts = gTTS(text=text_input, lang=LANGUAGES[tts_lang], slow=False)
                            audio_file = BytesIO()
                            tts.write_to_fp(audio_file)
                            audio_file.seek(0)
                            
                            # Show playing animation
                            animation_placeholder.markdown("""
                            <div class="fullscreen-animation">
                                <div class="studio-mic">
                                    <div class="mic-stand"></div>
                                    <div class="mic-base"></div>
                                    <div class="mic-head" style="animation: pulse 0.8s infinite, glow 1s infinite;">🔊</div>
                                </div>
                                <div class="sound-waves">
                                    <div class="wave"></div>
                                    <div class="wave"></div>
                                    <div class="wave"></div>
                                    <div class="wave"></div>
                                    <div class="wave"></div>
                                </div>
                                <div class="status-text">Playing audio...</div>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Play audio and estimate duration
                            st.audio(audio_file, format='audio/mp3')
                            word_count = len(text_input.split())
                            duration = max(3, word_count / (voice_speed/100 * 2.9))
                            time.sleep(duration)
                            
                            # Remove animation after playback
                            animation_placeholder.empty()
                            
                        except Exception as e:
                            animation_placeholder.empty()
                            st.error(f"❌ Could not generate speech: {e}")
                else:
                    st.warning("⚠️ Please enter some text first")

        with btn_col2:
            if st.button("📥 Download Audio", key="download_audio"):
                if text_input:
                    with st.spinner("Generating audio file..."):
                        try:
                            tts = gTTS(text=text_input, lang=LANGUAGES[tts_lang], slow=False)
                            audio_bytes = BytesIO()
                            tts.write_to_fp(audio_bytes)
                            audio_bytes.seek(0)
                            
                            st.success("Audio ready for download!")
                            st.download_button(
                                label="💾 Download MP3",
                                data=audio_bytes,
                                file_name="text_to_speech.mp3",
                                mime="audio/mpeg",
                                key="final_download"
                            )
                        except Exception as e:
                            st.error(f"❌ Could not generate speech: {e}")
                else:
                    st.warning("⚠️ Please enter some text first")