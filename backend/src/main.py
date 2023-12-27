import io
import os
import tempfile

from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from midi2audio import FluidSynth
from starlette.responses import StreamingResponse

from src.guitartabstomidi.midi_generator import Track
from src.guitartabstomidi.read_tabs import Tabs
from src.schemas import CreateMidiRequest

app = FastAPI()


@app.post("/generate_midi")
async def generate_midi(
        create_midi_request: CreateMidiRequest
):
    midi_generator, midi_meta_data = await create_midi_tack(create_midi_request)

    file_like = await create_byte_object(midi_generator)

    def file_generator():
        while chunk := file_like.read(1024 * 1024):  # Read in chunks of 1 MB
            yield chunk

    return StreamingResponse(file_generator(), headers = {
        'Content-Disposition': 'attachment; filename="output.mid"'
    }, media_type = "audio/midi")


@app.post("/generate_audio")
async def generate_audio(
        create_midi_request: CreateMidiRequest
):
    midi_generator, midi_meta_data = await create_midi_tack(create_midi_request)

    def mp3_generator():
        # with tmp file
        with tempfile.TemporaryDirectory() as tmp_dir:
            # Path for the temporary MIDI file
            tmp_midi_path = os.path.join(tmp_dir, "tempfile.midi")
            # Create and write to the MIDI file
            with open(tmp_midi_path, "wb") as tmp_midi_file:
                midi_generator.writeFile(tmp_midi_file)

            # Path for the temporary MP3 file
            tmp_mp3_path = os.path.join(tmp_dir, "tempfile.mp3")
            # Convert MIDI to MP3

            FluidSynth(sound_font = os.path.join(os.path.dirname(__file__), "..", "midi_font", "sound_font.sf2")).midi_to_audio(tmp_midi_path, tmp_mp3_path)

            with open(tmp_mp3_path, "rb") as tmp_mp3_file:
                while chunk := tmp_mp3_file.read(1024 * 1024):
                    yield chunk

    return StreamingResponse(mp3_generator(), headers = {
        'Content-Disposition': 'attachment; filename="output.mp3"'
    }, media_type = "audio/mpeg")


async def create_midi_tack(create_midi_request):
    tab = create_midi_request.tab
    # check if tab is valid
    if tab is None or len(tab) == 0 or len(tab.splitlines()) != 6:
        raise HTTPException(status_code = 400, detail = "Invalid tab")
    tempo = create_midi_request.tempo
    t = Tabs(tab)
    t.preprocess()
    if create_midi_request.verbose:
        t.displayTabs()
    t.convertNotes()
    output_track = Track(int(tempo))
    midi_generator, midi_meta_data = output_track.midiGenerator(t.a)
    return midi_generator, midi_meta_data


async def create_byte_object(midi_generator):
    file_like = io.BytesIO()
    midi_generator.writeFile(file_like)
    file_like.seek(0)
    return file_like
