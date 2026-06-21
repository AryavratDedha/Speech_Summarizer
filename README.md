# AI Notes Summarizer

Record your voice and get a transcript + structured AI-generated notes.

## How it works

1. Record audio directly in the browser
2. Transcribed locally using `faster-whisper`
3. Summarized into structured notes using Groq's `llama-3.1-8b-instant`

## Setup

Requires a `GROQ_API_KEY` set as a Space secret (Settings → Variables and secrets).

## Stack

- Streamlit (UI)
- faster-whisper (speech-to-text)
- Groq API (summarization)
