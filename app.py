import streamlit as st
from streamlit_lottie import st_lottie
import requests
import wave
import struct
from pvrecorder import PvRecorder
import cv2
from PIL import Image
import numpy as np
import speech_recognition as sr
from gtts import gTTS
import os
import tempfile
import time
import sounddevice as sd
import pyaudio

# Set page config (must be the first Streamlit command)
st.set_page_config(layout="wide", page_title="ASL Translator", page_icon="🤟")

# Function to load Lottie animation
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Custom CSS
st.markdown("""
<style>
    .main {
        background-color: #f0f8ff;
    }
    .big-font {
        font-size: 3.5rem !important;
        font-weight: 700;
        color: #1e3a8a;
        text-align: center;
        margin-bottom: 1rem;
    }
    .subtitle {
        font-size: 1.5rem;
        color: #4a5568;
        text-align: center;
        margin-bottom: 2rem;
    }
    .card {
        border-radius: 10px;
        padding: 1.5rem;
        background-color: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease-in-out;
    }
    .card:hover {
        transform: translateY(-5px);
    }
    .card h3 {
        color: #2c5282;
        font-size: 1.5rem;
        margin-bottom: 1rem;
    }
    .card p {
        color: #4a5568;
    }
    .btn-primary {
        background-color: #3b82f6;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        text-decoration: none;
        font-weight: bold;
        display: inline-block;
        margin-top: 1rem;
        transition: background-color 0.3s ease-in-out;
    }
    .btn-primary:hover {
        background-color: #2563eb;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.markdown(
    """
    <div style='text-align: center; padding: 1rem; background-color: #3b5998; color: white; border-radius: 5px;'>
        <h2 style='margin-bottom: 0;'>ASL Translator</h2>
        <p style='margin-top: 0;'>Breaking barriers in communication</p>
    </div>
    """,
    unsafe_allow_html=True
)
st.sidebar.image('static/ASL.jpg', use_container_width=True)
option = st.sidebar.selectbox(
    'Select Mode:',
    ('Home', 'ASL to Text', 'Audio to Text')
)

# Home page content
if option == 'Home':
    # Title and subtitle
    st.markdown("<h1 class='big-font'>American Sign Language Translator</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>Breaking communication barriers with technology</p>", unsafe_allow_html=True)

    # Main content
    col1, col2 = st.columns([3, 2])

    with col1:
        # Lottie animation
        lottie_url = "https://assets5.lottiefiles.com/packages/lf20_26ewjioz.json"
        lottie_json = load_lottieurl(lottie_url)
        if lottie_json:
            st_lottie(lottie_json, height=400)
        else:
            st.image('static/ASL.jpg', use_column_width=True)

    with col2:
        st.markdown("""
        <div class='card'>
            <h3>What is ASL Translator?</h3>
            <p>ASL Translator is an innovative tool designed to bridge the communication gap between sign language users and others. Our application uses cutting-edge technology to translate American Sign Language gestures into text and convert spoken words into text, making communication more inclusive and accessible.</p>
        </div>
        """, unsafe_allow_html=True)

    # Features section
    st.markdown("<h2 style='text-align: center; color: #2c5282; margin-top: 2rem;'>Features</h2>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class='card'>
            <h3>ASL to Text</h3>
            <p>Translate American Sign Language gestures into text using your camera. Our advanced AI model recognizes hand movements and converts them into readable text in real-time.</p>
             
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class='card'>
            <h3>Audio to Text</h3>
            <p>Convert spoken words into text using your microphone. This feature enables easy transcription of speech, making it accessible for those who communicate primarily through text.</p>
            
        </div>
        """, unsafe_allow_html=True)

    # About section
    st.markdown("<h2 style='text-align: center; color: #2c5282; margin-top: 2rem;'>About Us</h2>", unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align: center; max-width: 800px; margin: 0 auto;'>
        <p>We are passionate about creating technology that makes a positive impact on people's lives. Our team of developers and  designers work tirelessly to improve communication for everyone, regardless of their abilities.</p>
    </div>
    """, unsafe_allow_html=True)

elif option == "ASL to Text":
    st.markdown("<h1 class='big-font'>Real-Time ASL Detection</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>Use your camera to translate ASL gestures into text</p>", unsafe_allow_html=True)

     # Initialize session state for video capture
    if 'cap' not in st.session_state:
        st.session_state.cap = None
    if 'is_recording' not in st.session_state:
        st.session_state.is_recording = False
    if 'video_writer' not in st.session_state:
        st.session_state.video_writer = None

    # Placeholder for video frame
    frame_placeholder = st.empty()

    # Video recording settings
    output_file = "recorded_video.avi"  # Output video file name
    frame_width = 640
    frame_height = 480
    fps = 30
    fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Codec for .avi files

    # Start Camera button logic
    if not st.session_state.is_recording:
        start_button = st.button("Start Camera and Record Video")

        if start_button:
            st.session_state.is_recording = True  # Start recording
            st.session_state.cap = cv2.VideoCapture(0)  # Initialize webcam
            st.session_state.cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
            st.session_state.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)
            st.session_state.cap.set(cv2.CAP_PROP_FPS, fps)

            # Initialize the video writer
            st.session_state.video_writer = cv2.VideoWriter(
                output_file, fourcc, fps, (frame_width, frame_height)
            )

    # Stop Camera button logic
    if st.session_state.is_recording:
        stop_button = st.button("Stop Camera")

        if stop_button:
            st.session_state.is_recording = False  # Stop recording
            if st.session_state.cap is not None:
                st.session_state.cap.release()  # Release the webcam
            if st.session_state.video_writer is not None:
                st.session_state.video_writer.release()  # Release the video writer
            

        # Capture and display video frames
        if st.session_state.cap is not None and st.session_state.cap.isOpened():
            while st.session_state.is_recording:
                ret, frame = st.session_state.cap.read()
                if ret:
                    # Write frame to video file
                    st.session_state.video_writer.write(frame)

                    # Display the frame in the app
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    frame_placeholder.image(frame_rgb, channels="RGB", use_container_width=True)
                else:
                    st.error("Failed to capture video frame.")
                    st.session_state.is_recording = False
                    if st.session_state.cap is not None:
                        st.session_state.cap.release()
                    if st.session_state.video_writer is not None:
                        st.session_state.video_writer.release()
                    break

                time.sleep(0.03)
    

    # Placeholder for ASL translation result
    st.subheader("Translated Text:")
    Translated_text = 'Translated_text Appears here'
    st.markdown(
        f"""
        <div class='output-area'>
            <p style="font-size: 18px; color: #3b5998;">{Translated_text}.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

elif option == "Audio to Text":
    st.markdown("<h1 class='big-font'>Real-time Audio to Text Conversion</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>Use your microphone to convert speech to text</p>", unsafe_allow_html=True)

    path = ('H:\QUEENS UNIVERSITY\QHACKS\SignFlow\Recorded_audio.wav')

            
        # Set up Streamlit interface
    
    st.write("Click the button below to start recording and stop it when you are done.")

    # Session state variables to track recording state
    if 'is_recording' not in st.session_state:
        st.session_state.is_recording = False
    if 'audio_data' not in st.session_state:
        st.session_state.audio_data = []

    def start_recording():
        st.session_state.is_recording = True
        st.write("Recording started... Speak into the microphone.")
        st.image('static/recording.png')
        
        sample_rate = 16000  # Sample rate in Hz
        channels = 1  # Mono audio
        frames_per_buffer = 1024  # Frames per buffer for real-time capture

        # Initialize pyaudio
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16,
                        channels=channels,
                        rate=sample_rate,
                        input=True,
                        frames_per_buffer=frames_per_buffer)

        st.session_state.audio_data = []

        try:
            while st.session_state.is_recording:
                audio_frame = stream.read(frames_per_buffer)
                st.session_state.audio_data.append(audio_frame)

            st.write("Recording stopped.")
            
            # Save the recorded audio to the file
            with wave.open(path, 'wb') as f:
                f.setparams((1, 2, sample_rate, len(st.session_state.audio_data)*frames_per_buffer, 'NONE', 'NONE'))  # Mono, 16-bit, 16000 Hz
                for frame in st.session_state.audio_data:
                    f.writeframes(frame)

            st.write(f"Audio saved successfully at {path}")
        except Exception as e:
            st.error(f"An error occurred: {e}")
        finally:
            stream.stop_stream()
            stream.close()

    # Display the buttons
    start_button = st.button("Start Recording")
    stop_button = st.button("Stop Recording")

    if start_button and not st.session_state.is_recording:
        start_recording()

    if stop_button and st.session_state.is_recording:
        st.session_state.is_recording = False
        st.write("Recording stopped manually.")
        # Save the audio
        with wave.open(path, 'wb') as f:
            f.setparams((1, 2, 16000, len(st.session_state.audio_data)*1024, 'NONE', 'NONE'))  # Mono, 16-bit, 16000 Hz
            for frame in st.session_state.audio_data:
                f.writeframes(frame)
    # Audio recording settings
    # Placeholder for speech-to-text result
    st.subheader("Converted Text:")
    converted_text = 'Appears here'
    st.markdown(
        f"""
        <div class='output-area'>
            <p style="font-size: 18px; color: #3b5998;">{converted_text}.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# Footer
st.markdown(
    """
    <div style='text-align: center; margin-top: 2rem; padding: 1rem; background-color: #2c5282; color: white;'>
        <p>© 2025 ASL Translator. All rights reserved.</p>
    </div>
    """,
    unsafe_allow_html=True
)

