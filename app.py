import streamlit as st
import tempfile
from faster_whisper import WhisperModel
from groq import Groq

GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

st.set_page_config(page_title="AI Notes Summarizer", page_icon="📝")
st.title("📝 AI Notes Summarizer")
st.write("Record your voice and get structured notes instantly.")


@st.cache_resource
def load_model():
    return WhisperModel("small", device="cpu", compute_type="int8")


def transcribe_audio(audio_file):
    model = load_model()
    segments, _ = model.transcribe(audio_file, language="en")
    text = ""
    for segment in segments:
        text += segment.text
    return text


def summarize_transcript(transcript):
    client = Groq(api_key=GROQ_API_KEY)
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": (
                    "You convert spoken transcripts into clean, structured notes "
                    "with headings and bullet points. Be concise and organize by topic."
                ),
            },
            {"role": "user", "content": transcript},
        ],
    )
    return response.choices[0].message.content


audio_value = st.audio_input("Record your notes")

if audio_value is not None:
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        tmp.write(audio_value.getvalue())
        tmp_path = tmp.name

    with st.spinner("Transcribing..."):
        transcript = transcribe_audio(tmp_path)

    with st.spinner("Summarizing..."):
        summary = summarize_transcript(transcript)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Full Transcript")
        st.write(transcript)
    with col2:
        st.subheader("Structured Summary")
        st.markdown(summary)