from flask import render_template, flash, redirect
from app import app
from app.forms import YoutubeForm
from youtube_transcript_api import YouTubeTranscriptApi

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
