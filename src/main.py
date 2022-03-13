import os
import asyncio
from typing import Tuple, List

import moviepy.editor as mp
from deepgram import Deepgram
from rich import print

from conf import IMAGEMAGIK_LOCATION, DEEPGRAM_KEY, CONFIG

# Required for Windows users
if os.name == "nt":
    # Thanks to https://www.reddit.com/r/moviepy/comments/98sazz/comment/ebusacu
    from moviepy.config import change_settings
    change_settings({"IMAGEMAGICK_BINARY": IMAGEMAGIK_LOCATION})


class DeepSub:
    """
    Subtitle Maker
    ~~~~~~~~~~~~~~~~~~~~
    Takes a video and renders subtitles onto it. Powered by Deepgram.
    Made by Dhravya Shah for Deepgram Hackathon by dev.to.

    Requires moviepy, deepgram, and imagemagik.

    Use render_subtitles() to render the subtitles on the video.
    """

    # TODO: FIX OVERLAPPING OF SUBTITLES
    # TODO: Make it faster

    def __init__(self, video_path: os.PathLike) -> None:

        try:
            self.video = mp.VideoFileClip(video_path, audio=CONFIG["AUDIO"])
            self.video_path = video_path
        except OSError:
            print("[bold red]Video not found.[/bold red] Exiting...")
            exit()
        
        self.__config_check()

        # I'm using a composite video clip to render the subtitles on the video
        self.final_so_far = self.video

        print(
            """
[green]

  _   ___    __                    __   __  _ __  __      _____                      __          
 | | / (_)__/ /__ ___    ___ __ __/ /  / /_(_) /_/ /__   / ___/__ ___  ___ _______ _/ /____  ____
 | |/ / / _  / -_) _ \  (_-</ // / _ \/ __/ / __/ / -_) / (_ / -_) _ \/ -_) __/ _ `/ __/ _ \/ __/
 |___/_/\_,_/\__/\___/ /___/\_,_/_.__/\__/_/\__/_/\__/  \___/\__/_//_/\__/_/  \_,_/\__/\___/_/   
                                                                                                 
[bold blue]Deepgram Hackathon submission by [yellow]Dhravya Shah[/yellow][/bold blue]
[/green]
        """
        )

        print(f"[bold blue]Using Video path: [/bold blue] {self.video_path}")

    async def get_subtitles(self) -> List[Tuple[float, str]]:
        """Runs the video path through Deepgram and returns the subtitles as a list of tuples."""
        # Initialises Deepgram
        dg_client = Deepgram(DEEPGRAM_KEY)

        with open(self.video_path, "rb") as f:
            video_data = f.read()


        source = {"buffer": video_data, "mimetype": "video/mp4"}
        options = {"punctuate": True, "language": "en-US"}

        print("⚡ Fetching the Video Transcripts from [red]Deepgram[/red]")
        response = await dg_client.transcription.prerecorded(source, options)

        print(
            "✅ [green]Deepgram has sent back the subtitles.[/green] [blue]I will now process them and render them on the video.[/blue]"
        )

        subtitles = []

        # Iterates through the response and creates a list of tuples
        for word in response["results"]["channels"][0]["alternatives"][0]["words"]:
            start_time, word = word["start"], word["word"]

            start_time = round(start_time, 3)

            subtitles.append((start_time, word))

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
        print("[bold blue]Rendering has [green]started.[/green][/bold blue]")

        w, h = moviesize = self.video.size

        display_str = ""
        for t, text in subtitles:
            display_str = (
                display_str + (text + " ") if len(display_str.split(" ")) < 10 else text
            )
            txt_col = self._text_generator(display_str)

            # Endtime is the value of the next subtitle to come
            index_of_t = subtitles.index((t, text))
            end_time = (
                subtitles[int(index_of_t) + 1][0]
                if index_of_t + 1 < len(subtitles)
                else subtitles[int(index_of_t)][0]
            )

            # Sets the end and start time for timing
            txt_col = txt_col.set_end(end_time)
            txt_col = txt_col.set_start(t)

            #  Adds the text clip to the final video
            txt_mov = txt_col.set_position((w / 4, h - txt_col.h - int(h / 30) - 20))

            # Composite the text clip onto the video
            self.final_so_far = mp.CompositeVideoClip([self.final_so_far, txt_mov])

        print(
            f"""Writing the video file to [bold blue]{CONFIG["OUTPUT_FILE"]}[/bold blue].
        
        Saving with the following settings:
        
        [green]FPS:[/green] [blue]{CONFIG['OUTPUT_FPS']}[/blue]
        [green]Resolution:[/green] [blue]{w}x{h}[/blue]
        [green]Audio:[/green] [blue]{CONFIG["AUDIO"]}[/blue]
        [green]Video Codec:[/green] [blue]{CONFIG["VIDEO_CODEC"]}[/blue]

        Sit back and relax. This may take a while.

        💡[italic yellow]You can change the settings in conf.py[/italic yellow] 
        """
        )
        # Saves the final video
        self.final_so_far.write_videofile(
            CONFIG["OUTPUT_FILE"],
            fps=CONFIG["OUTPUT_FPS"],
            codec=CONFIG["VIDEO_CODEC"],
            temp_audiofile="tmp.mp3",
            remove_temp=True,
        )

    def __config_check(self) -> None:
        """
        Checks the config file for correct values
        """

        if not all(thing in CONFIG for thing in ["OUTPUT_FPS", "AUDIO", "VIDEO_CODEC", "OUTPUT_FILE"]):
            print(
                f"[bold red]Please check your config file. The following keys are missing:[/bold red]\n"
            )
            for thing in ["OUTPUT_FPS", "AUDIO", "VIDEO_CODEC", "OUTPUT_FILE"]:
                if thing not in CONFIG.keys():
                    print(f"{thing}")
            exit()

        # Checks if output_fps is an integer
        if not isinstance(CONFIG["OUTPUT_FPS"], int):
            print(
                f"[bold red]Please check your config file. The [italic blue]OUTPUT_FPS[/italic blue] key must be an integer.[/bold red]"
            )
            exit()

        # Checks if audio is a boolean
        if not isinstance(CONFIG["AUDIO"], bool):
            print(
                f"[bold red]Please check your config file. The [italic blue]AUDIO[/italic blue] key must be a boolean.[/bold red]"
            )
            exit()

        # Checks if video_codec is in the list of allowed codecs
        if CONFIG["VIDEO_CODEC"] not in ["libx264", "mpeg4", "rawvideo", "libvpx"]:
            print(
                f"[bold red]Please check your config file. The [italic blue]VIDEO_CODEC[/italic blue] key must be one of the following: [italic green]libx264, mpeg4, rawvideo, libvpx[/italic green]. You have entered: [italic blue]{CONFIG['VIDEO_CODEC']}[/italic blue]. [/bold red]"
            )
            exit()
        
        # Checks if output_file is a valid path
        if not (CONFIG["OUTPUT_FILE"].endswith(".mp4") or CONFIG["OUTPUT_FILE"].endswith(".mov")):
            print(
                f"[bold red]Please check your config file. The [italic blue]OUTPUT_FILE[/italic blue] key must be a valid path to a .mp4 or .mov file.[/bold red]"
            )
            exit()

if __name__ == "__main__":
    sm = DeepSub("t.mp4")
    loop = asyncio.get_event_loop()
    s = loop.run_until_complete(sm.get_subtitles())
    sm.render_subtitles(s)
