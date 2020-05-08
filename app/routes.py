from flask import render_template, flash, redirect
from app import app
from app.forms import YoutubeForm, VideoForm
from youtube_transcript_api import YouTubeTranscriptApi
from werkzeug.utils import secure_filename
import os
from app.audio import extract_audio
from app.ibm import transcribe
from app.speakers import get_transcript

def extract_lines(data):
    return [a['text'] for a in data]
    

@app.route('/',methods=['GET', 'POST'])
@app.route('/index',methods=['GET', 'POST'])
def index():
    utterances = ["Sentence 1","Sentence 2","Sentence 3"]
    form = YoutubeForm()
    default_val = 'I0mxnyp2kBw'
    trv = YouTubeTranscriptApi.get_transcript(default_val)
    utterances = extract_lines(trv)
    if form.validate_on_submit():
        vidId = form.yt_url.data
        trv = YouTubeTranscriptApi.get_transcript(vidId)
        utterances = extract_lines(trv)
        return render_template('index.html',utterances=utterances,form=form,vidId=vidId)
    return render_template('index.html',utterances=utterances,form=form,vidId='I0mxnyp2kBw')

@app.route('/video',methods=['GET', 'POST'])
def video():
    utterances = ["Nothing to diplay yet!", "Just upload a file"]
    form = VideoForm()
    if form.validate_on_submit():
        f = form.vid.data
        #filename = secure_filename(f.filename)
        filename = 'video.mp4'
        filepath = os.path.join(
            app.instance_path, filename)
        full_filename = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        f.save(full_filename)
        audio_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'theaudio.mp3')
        
        extract_audio(filename=full_filename,out=audio_filename)
        
        data = transcribe(audio_filename)
        print(type(data))
        transcript = get_transcript(data)
        utterances = [ "Speaker: "+str(t['speaker'])+" "+t['transcript'] for t in transcript]
        return render_template('video.html',utterances=utterances,form=form,filename=filename)
    return render_template('video.html',utterances=utterances,form=form)
