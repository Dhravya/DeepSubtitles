import os
import asyncio
from typing import Tuple, List

import moviepy.editor as mp
from deepgram import Deepgram

from conf import IMAGEMAGIK_LOCATION, DEEPGRAM_KEY

# Required for Windows users
if os.name == "nt":
    from moviepy.config import change_settings

    change_settings({"IMAGEMAGICK_BINARY": IMAGEMAGIK_LOCATION})


class SubtitleMaker:
    """
    Subtitle Maker
    ~~~~~~~~~~~~~~~~~~~~
    Takes a video and renders subtitles onto it. Powered by Deepgram.
    Made by Dhravya Shah

    Use render_subtitles() to render the subtitles on the video.
    """

    def __init__(self, video_path: os.PathLike) -> None:

        self.video_path = video_path
        self.video = mp.VideoFileClip(video_path, audio=True)
        self.final_so_far = self.video

    async def __get_subtitles(self) -> List[Tuple[float, str]]:
        """Runs the video path through Deepgram and returns the subtitles as a list of tuples."""
        dg_client = Deepgram(DEEPGRAM_KEY)

        with open(self.video_path, "rb") as f:
            video_data = f.read()

        source = {"buffer": video_data, "mimetype": "video/mp4"}
        options = {"punctuate": True, "language": "en-US"}

        print("Running Deepgram...")
        response = await dg_client.transcription.prerecorded(source, options)

        print("Deepgram finished.")

        subtitles = []

        for word in response["results"]["channels"][0]["alternatives"][0]["words"]:
            start_time, word = word["start"], word["word"]

            start_time = round(start_time, 3)

            subtitles.append((start_time, word))

        return subtitles

    def get_subtitles(self) -> List[Tuple[float, str]]:
        """Runs the video path through Deepgram and returns the subtitles as a list of tuples."""

        loop = asyncio.get_event_loop()
        subtitles = loop.run_until_complete(self.__get_subtitles())
        return subtitles

    def _text_generator(self, text: str) -> mp.TextClip:
        """
        Generates a text clip with the given text.

        :param text: The text to be displayed.
        :return: A text clip.
        """

        # Creates the textclip object
        my_text = mp.TextClip(text, font="Amiri-regular", color="white", fontsize=15)

        # Creates the background clip
        txt_col = my_text.on_color(
            size=(my_text.w + 20, my_text.h + 5),
            color=(0, 0, 0),
            pos=(6, "center"),
            col_opacity=0.3,
        )
        return txt_col

    def render_subtitles(self, subtitles: List[Tuple[float, str]]) -> None:
        """
        Gets the text clip and renders it on the video.

        :return: None

        Subtitles have to be in the form of a list of tuples.
        e.g.

        >>> subtitles = [
                (0.0, "Hello"),
                (1.0, "World"),
                (2.0, "!"),
            ]
        """

        w, h = moviesize = self.video.size

        display_str = ""
        for t, text in subtitles:
            display_str = (
                display_str + (text + " ") if len(display_str.split(" ")) < 10 else text
            )
            txt_col = self._text_generator(display_str)

            # Endtime is the value of the next subtitle to come
            end_time = subtitles[int(t) + 1][0] if t + 1 < len(subtitles) else t

            # Sets the end and start time for timing
            txt_col = txt_col.set_end(end_time)
            txt_col = txt_col.set_start(t)

            #  Adds the text clip to the final video
            txt_mov = txt_col.set_position((w / 4, h - txt_col.h - int(h / 30) - 20))

            # Composite the text clip onto the video
            self.final_so_far = mp.CompositeVideoClip([self.final_so_far, txt_mov])

        # Saves the final video
        self.final_so_far.write_videofile(
            "final.mp4",
            fps=24,
            codec="libx264",
            temp_audiofile="tmp.mp3",
            remove_temp=True,
        )


if __name__ == "__main__":
    sm = SubtitleMaker("test.mp4")
    s = sm.get_subtitles()
    sm.render_subtitles(s)
