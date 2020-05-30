from flask import render_template, flash, redirect, request, make_response, jsonify
from app import app
from app.forms import YoutubeForm, VideoForm
from youtube_transcript_api import YouTubeTranscriptApi
from werkzeug.utils import secure_filename
import os
from app.audio import extract_audio
from app.ibm import transcribe_audio
from app.speakers import get_transcript

def extract_lines(data):
    return [a['text'] for a in data]
    

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    utterances = ["Nothing to diplay yet!", "Just upload a file"]
    form = VideoForm()
    if form.validate_on_submit():
        f = form.vid.data

        filename = 'video.mp4'
        filepath = os.path.join(
            app.instance_path, filename)
        full_filename = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        f.save(full_filename)
        audio_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'theaudio.mp3')
        
        extract_audio(filename=full_filename,out=audio_filename)
        
        data = transcribe_audio(audio_filename)
        
        transcript = get_transcript(data)
        utterances = [ "Speaker "+str(t['speaker'])+": "+t['transcript'] for t in transcript]
        return render_template('index.html',utterances=utterances,form=form,filename=filename)
    return render_template('index.html',utterances=utterances,form=form,filename="standby.mp4")

@app.route("/upload-video", methods=["GET", "POST"])
def upload_video():

    if request.method == "POST":

        file = request.files["file"]

        print("File uploaded")
        print(file)

        res = make_response(jsonify({"message": "File uploaded", 'video':secure_filename(file.filename)}), 200)

        if file:
            filename = secure_filename(file.filename)
            full_filename = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            app.config['FILENAME'] = full_filename
            file.save(full_filename)
        return res

    return render_template("upload.html")

@app.route("/transcribe", methods=["POST"])
def transcribe():
    audio_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'theaudio.mp3')
    full_filename = app.config['FILENAME']
    extract_audio(filename=full_filename,out=audio_filename)
    
    data = transcribe_audio(audio_filename)
    
    transcript = get_transcript(data)
    utterances = [ "Speaker "+str(t['speaker'])+": "+t['transcript'] for t in transcript]
    return jsonify({'text': utterances})