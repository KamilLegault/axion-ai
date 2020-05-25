from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import DataRequired

class YoutubeForm(FlaskForm):
    yt_url = StringField('URLS',default="I0mxnyp2kBw",validators=[DataRequired()])
    submit = SubmitField('Transcribe')

class VideoForm(FlaskForm):
    vid = FileField(u'Select a file (MP4 ONLY):', validators=[
        FileRequired(),
        FileAllowed(['mp4'], 'MP4 Video format only!')
        ])
    submit = SubmitField('Transcribe')
