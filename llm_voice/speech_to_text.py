from nicegui import ui, Client
from audio_recorder import AudioRecorder


def on_audio_ready(audio_data):
    ui.notify(f"Audio ready: {audio_data.args}")


@ui.page("/")
async def index(client: Client):

    audio_recorder = AudioRecorder(on_audio_ready=on_audio_ready)

    ui.button('Play', on_click=audio_recorder.play_recorded_audio)


ui.run()
