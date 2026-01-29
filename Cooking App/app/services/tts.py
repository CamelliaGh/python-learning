"""Text-to-speech service for generating audio from text using gTTS."""

from io import BytesIO

from gtts import gTTS


def generate_tts_audio(text):
    """Generate text-to-speech audio from the provided text.

    Args:
        text: The text to convert to speech audio.

    Returns:
        BytesIO: Audio stream containing the generated speech.

    Raises:
        ValueError: If no text is provided.
    """
    if text:
        tts = gTTS(text)
        audio_io = BytesIO()
        tts.write_to_fp(audio_io)
        audio_io.seek(0)
        return audio_io
    else:
        raise ValueError("No text provided")
