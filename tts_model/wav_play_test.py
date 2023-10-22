from pydub import AudioSegment
from pydub.playback import play
import io

data = r'RIFF2�'
file = io.BytesIO(data)
# with open("sound.wav", "wb") as f:
#     f.write(data)

# song = AudioSegment.from_file("sound.wav", format="wav")
# play(song)
import simpleaudio as sa

with open("sound.wav", "rb") as f:
    data = f.read()
    play_obj = sa.play_buffer(data, 1, 1, 44100)