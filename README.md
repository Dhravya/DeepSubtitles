<img src="./assets/logo.png" alt="DeepSubtitles Logo" style="float: left; margin: 0 10px 0 0;" align="left" height="150" width="150">

## DeepSubtitles

A Python script that generates subtitles and renders them to the video.
> This was made as a submission for the [DeepGram x Dev](https://dev.to/devteam/join-us-for-a-new-kind-of-hackathon-on-dev-brought-to-you-by-deepgram-2bjd) Hackathon

***
<br><br>

## Here's a Demo 👀
<img src="https://j.gifs.com/57wQ8v.gif" width="400" align="center">

## What it does:

- Takes a video file's path as the input
- Generates Subtitles from the video's contents
- Renders them onto the video

Goal of this project was to provide accessibility to the video for people with disabilities.

## Features

- 💯 Accurate subtitles, powered by [Deepgram](https://deepgram.com/)
- ⚡ Customisable
- 👀 Heavily commented and documented code

One Caveat is that it's not a fast script and probably not ideal for a production environment.

If you have any questions, please feel free to reach out to me, if you'd like to contribute to this project, feel free to make an issue on [Github](https://github.com)

## Installation and Usage

Clone this repository and download the requirements:
```shell
git clone https://github.com/Dhravya/DeepSubtitles
cd DeepSubtitles
pip install -r requirements.txt
```

Then, go to src/conf.py and enter your Deepgram API key.

> Get the key from [Here](https://deepgram.com/account/api)

Make sure to change the `video_path` variable to the path of the video you want to process.

And finally, run the script:
```shell
python src/main.py
```
