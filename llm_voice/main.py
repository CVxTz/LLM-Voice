from audio_recorder import AudioRecorder
from nicegui import run, ui

from llm_voice.llm import call_llm
from llm_voice.stt import transcribe_audio


class PageData:
    def __init__(self):
        self.audio_byte64 = None
        self.prompt = "Speak while holding the button and your prompt will appear here!"
        self.response = "The LLM will respond here."
        self.response_html = self.response
        self.response_audio = ""

    async def run_workflow(self, audio_data):
        self.prompt = "Transcribing audio..."
        self.response_html = ""
        self.audio_byte64 = audio_data.args["audioBlobBase64"]
        self.prompt = await run.io_bound(
            callback=transcribe_audio, base64_audio=self.audio_byte64
        )
        self.response_html = "Calling LLM..."
        self.response = await run.io_bound(callback=call_llm, prompt=self.prompt)
        self.response_html = self.response.replace("\n", "</br>")
        ui.notify("Result Ready!")


@ui.page("/")
async def index():
    page_data = PageData()

    row_1 = ui.row().classes("w-full justify-center")
    row_2 = ui.row().classes("w-full justify-center")
    row_3 = ui.row().classes("w-full justify-center")

    with row_1:
        AudioRecorder(on_audio_ready=page_data.run_workflow)

    with row_2:
        with ui.column():
            ui.label("Prompt:")

            ui.label().bind_text_from(page_data, "prompt").classes(
                "text-lg sm:text-2xl text-gray-800 bg-gray-100 rounded-lg shadow-lg p-6"
            )

    with row_3:
        with ui.column():
            ui.label("Response:")

            ui.html().bind_content(page_data, "response_html").classes(
                "text-lg sm:text-2xl text-gray-800 bg-gray-100 rounded-lg shadow-lg p-6"
            )


ui.run()
