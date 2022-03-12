import moviepy.editor as mp
from moviepy.config import change_settings
from conf import IMAGEMAGIK_LOCATION as IL

change_settings({"IMAGEMAGICK_BINARY": IL})

my_video = mp.VideoFileClip("rickroll.mp4", audio=True)

w, h = moviesize = my_video.size

subtitles = {0:"This is the start", 10:"This is the end"}

def text_generator(text):
    my_text = mp.TextClip(
        text, font="Amiri-regular", color="white", fontsize=34
    )
    txt_col = my_text.on_color(
        size=(my_video.w + my_text.w, my_text.h + 5),
        color=(0, 0, 0),
        pos=(6, "center"),
        col_opacity=0.0,
    )
    return txt_col

txt_col = text_generator("Rick Astley - Never Gonna Give You Up")

def pos(t: float):
    return (max(w / 30, int(w - 0.5 * w * 4)), h - txt_col.h - int(h / 30))

txt_mov = txt_col.set_pos(pos)

final = mp.CompositeVideoClip([my_video, txt_mov])

final.subclip(0, 17).write_videofile("final.mp4", fps=24, codec="libx264")
