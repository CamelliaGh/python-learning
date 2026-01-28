"""Text-to-speech API routes for converting text to audio."""

from io import BytesIO

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import StreamingResponse

from app.services.tts import generate_tts_audio

router = APIRouter()


@router.get("/api/tts")
def tts(text: str = Query("")):
    """Generate text-to-speech audio from the provided text.

    Args:
        text: The text to convert to speech audio.

    Returns:
        StreamingResponse: Audio stream in MPEG format.

    Raises:
        HTTPException: 400 if no text is provided, 500 if TTS generation fails.
    """
    if not text:
        raise HTTPException(status_code=400, detail="No text provided")

    audio = generate_tts_audio(text)

    if isinstance(audio, BytesIO):
        return StreamingResponse(audio, media_type="audio/mpeg")

    raise HTTPException(status_code=500, detail="Unsupported audio object from TTS")
