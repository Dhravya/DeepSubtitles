import os
from typing import Tuple, List

import moviepy.editor as mp
from moviepy.config import change_settings

from conf import IMAGEMAGIK_LOCATION

# Required for Windows users
change_settings({"IMAGEMAGICK_BINARY": IMAGEMAGIK_LOCATION})


class SubtitleMaker:
    """
    Subtitle Maker

    Use render_subtitles() to render the subtitles on the video.
    """

    def __init__(self, video_path:os.PathLike, subtitles: List[Tuple[float,str]]) -> None:
        self.video = mp.VideoFileClip(video_path, audio=True)
        self.subtitles = subtitles
        self.final_so_far = self.video

    def _text_generator(self, text:str) -> mp.TextClip:
        """
        Generates a text clip with the given text.

        :param text: The text to be displayed.
        :return: A text clip.
        """

        # Creates the textclip object 
        my_text = mp.TextClip(
            text, font="Amiri-regular", color="white", fontsize=15
        )

        # Creates the background clip
        txt_col = my_text.on_color(
            size=(my_text.w + 20, my_text.h + 5),
            color=(0, 0, 0),
            pos=(6, "center"),
            col_opacity=0.3,
        )
        return txt_col

    def render_subtitles(self) -> None:
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
        for t, text in self.subtitles:
            display_str = display_str + (text + " ") if len(display_str.split(" ")) < 10 else text
            txt_col = self._text_generator(display_str)

            # Endtime is the value of the next subtitle to come
            end_time =  self.subtitles[int(t)+1][0] if t+1 < len(self.subtitles) else 5
            
            # Sets the end and start time for timing
            txt_col = txt_col.set_end(end_time)
            txt_col = txt_col.set_start(t)

            #  Adds the text clip to the final video
            txt_mov = txt_col.set_position((w/4, h - txt_col.h - int(h / 30) - 20))

            # Composite the text clip onto the video
            self.final_so_far = mp.CompositeVideoClip([self.final_so_far, txt_mov])

        # Saves the final video
        self.final_so_far.subclip(0, 6).write_videofile("final.mp4", fps=24, codec="libx264", temp_audiofile="tmp.mp3", remove_temp=True)

if __name__ == "__main__":
    subtitles = [
        (0.0, "Hello"),
        (0.2, "Hello"),
        (0.4, "Hello"),
        (0.8, "Hello"),
        (1.0, "World"),
        (2.0, "!"),
    ]
    SubtitleMaker("rickroll.mp4", subtitles).render_subtitles()