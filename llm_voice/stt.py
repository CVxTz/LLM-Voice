import base64
import io
import pprint

import replicate

MODEL_STT = "openai/whisper"
VERSION = "4d50797290df275329f202e48c76360b3f22b08d28c196cbc54600319435f8d2"

ARGS = {
    "model": "large-v3",
    "language": "en",
    "translate": False,
    "temperature": 0,
    "transcription": "plain text",
    "suppress_tokens": "-1",
    "logprob_threshold": -1,
    "no_speech_threshold": 0.6,
    "condition_on_previous_text": True,
    "compression_ratio_threshold": 2.4,
    "temperature_increment_on_fallback": 0.2,
}


def transcribe_audio(base64_audio):
    audio_bytes = base64.b64decode(base64_audio)
    prediction = replicate.run(
        f"{MODEL_STT}:{VERSION}", input={"audio": io.BytesIO(audio_bytes), **ARGS}
    )
    text = "\n".join(segment["text"] for segment in prediction.get("segments", []))
    return text


if __name__ == "__main__":
    with open("audio.ogx", "rb") as f:
        content = f.read()

    _base64_audio = base64.b64encode(content).decode("utf-8")

    _prediction = transcribe_audio(_base64_audio)
    pprint.pprint(_prediction)
