from os import environ as env

from dotenv import load_dotenv
load_dotenv()

# Put your deepgram key here
DEEPGRAM_KEY = env.get("DEEPGRAM_KEY")

# This is for Windows users
IMAGEMAGIK_LOCATION= r"C:\Program Files\ImageMagick-7.1.0-Q16-HDRI\magick.exe"

CONFIG = {
    "OUTPUT_FPS": 24,
    "AUDIO" : True,
    "VIDEO_CODEC": "libx264",
    "OUTPUT_FILE": "output.mp4"
}