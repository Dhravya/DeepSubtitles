import moviepy.editor as mp
from moviepy.config import change_settings
from conf import IMAGEMAGIK_LOCATION as IL

change_settings({"IMAGEMAGICK_BINARY": IL})

my_video = mp.VideoFileClip("rickroll.mp4", audio=True)

w, h = moviesize = my_video.size

subtitles = [(5,"Get rickrolled lol"), (10,"This is the end")]

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

final_so_far = my_video

for t, text in subtitles:
    txt_col = text_generator(text)
    
    end_time =  subtitles[t+1][0] if t+1 < len(subtitles) else 5

    txt_col = txt_col.set_start(t)

    txt_mov = txt_col.set_position((max(w / 30, int(w - 0.5 * w * 4)), h - txt_col.h - int(h / 30)))
    final_so_far = mp.CompositeVideoClip([final_so_far, txt_mov])


final_so_far.subclip(0, 16).write_videofile("final.mp4", fps=24, codec="libx264")
