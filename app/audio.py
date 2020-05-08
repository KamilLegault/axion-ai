import moviepy.editor as mp

def extract_audio(filename='static/video.mp4',out='static/theaudio.mp3'):
    clip = mp.VideoFileClip(filename).subclip(0,120)
    clip.audio.write_audiofile(out)
