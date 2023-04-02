"""Services for the user app."""
from io import BytesIO
import openai
import os
from google.cloud import texttospeech

openai.api_key = os.environ.get("OPENAI_API_KEY")

def chat_gpt(input_text):
    """Send a message to ChatGPT and return the response."""
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"{input_text}\n\nChatGPT:",
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response.choices[0].text.strip()

def text_to_speech(text, filename):
    """Convert text to speech and save it to a file."""
    client = texttospeech.TextToSpeechClient()
    input_text = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL)
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)

    response = client.synthesize_speech(input=input_text, voice=voice, audio_config=audio_config)

    with open(filename, "wb") as out:
        out.write(response.audio_content)

class NamedBytesIO(BytesIO):
    """An in-memory file-like object that has a name attribute."""
    def __init__(self, data, name):
        super().__init__(data)
        self.name = name

def transcribe_audio_with_whisper(audio_data):
    """Transcribe an audio file using the Whisper ASR API."""
    # Create an in-memory file object from the audio data
    audio_file = NamedBytesIO(audio_data, "audio.webm")
    # Send the audio file to the Whisper ASR API
    response = openai.Audio.transcribe(
        "whisper-1",
        audio_file
    )
    # Extract the transcription from the response
    transcription = response['text'].strip()
    return transcription