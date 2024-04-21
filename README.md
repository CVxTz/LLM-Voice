# LLM-Voice


#  Whisper

```bash
docker run -it -p 9000:9000 -e ASR_MODEL=base -e ASR_ENGINE=openai_whisper onerahmet/openai-whisper-asr-webservice:latest
```

# Mimic 3 tts

```
mkdir -p "${HOME}/.local/share/mycroft/mimic3"
chmod a+rwx "${HOME}/.local/share/mycroft/mimic3"
docker run \
       -it \
       -p 59125:59125 \
       -v "${HOME}/.local/share/mycroft/mimic3:/home/mimic3/.local/share/mycroft/mimic3" \
       'mycroftai/mimic3'
```

https://github.com/rhasspy/piper

https://github.com/coqui-ai/TTS 