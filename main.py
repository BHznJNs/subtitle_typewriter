import os
from pydub import *
from moviepy import *

TEMP_DIR = "./temp/"
SOUND = "./resources/sfx-blipmale.wav"
FONT = "./resources/chinese.msyh.ttf"
FONT_SIZE = 144
STROKE_WIDTH = 6
ALIGNMENT = 'left'
EXTRA_DURATION = 2

def text_clip_factory(text: str, start: int | float, end: int | float) -> TextClip:
    TextClip.resized
    clip = TextClip(
        font=FONT,
        text=text,
        font_size=FONT_SIZE,
        color="#fff",
        stroke_color="#000",
        stroke_width=STROKE_WIDTH,
        text_align=ALIGNMENT,
        margin=(STROKE_WIDTH * 2, STROKE_WIDTH * 2),
    ).with_start(start)\
     .with_end(end)\
     .with_position('center')
    return clip

def generate_video_clip(text: str, char_duration_second: int | float) -> CompositeVideoClip:
    text_clips = []
    current_duration = 0
    for i, _ in enumerate(text):
        current_text = text[:i+1]
        text_clips.append(text_clip_factory(
            current_text,
            start=current_duration,
            end=current_duration + char_duration_second,
        ))
        current_duration += char_duration_second
    text_clips[-1] = text_clips[-1].with_duration(EXTRA_DURATION)
    last_clip_size = text_clips[-1].size
    final_video = CompositeVideoClip(text_clips, size=last_clip_size)
    return final_video

def generate_sound_clip(text: str, char_duration_second: int | float) -> str:
    sound = AudioSegment.from_file(SOUND)
    silence_duration_ms = char_duration_second * 1000 - len(sound)
    silence = AudioSegment.silent(duration=silence_duration_ms)
    pause = AudioSegment.silent(duration=char_duration_second * 1000)

    final_audio = AudioSegment.empty()
    for ch in text:
        if ch in [' ']:
            final_audio += pause
            continue
        final_audio += sound
        final_audio += silence

    temp_audio_path = TEMP_DIR + "temp.wav"
    final_audio.export(temp_audio_path, bitrate=130 * 1000, format="wav")
    return temp_audio_path

def write_video_clip(clip: CompositeVideoClip, output: str):
    clip.write_videofile(
        output,
        fps=60,
        codec="png",
        temp_audiofile_path=TEMP_DIR,
    )

if __name__ == "__main__":
    text = "Hello World!"
    output = "./{}.mov".format(text.replace('/', '-').replace('\\', '-'))
    char_duration = .2

    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR)

    audio_path = generate_sound_clip(text=text, char_duration_second=char_duration)
    clip = generate_video_clip(text=text, char_duration_second=char_duration).with_audio(AudioFileClip(audio_path))
    write_video_clip(clip, output=output)
