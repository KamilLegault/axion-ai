from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class YoutubeForm(FlaskForm):
    yt_url = StringField('URLS',default="I0mxnyp2kBw",validators=[DataRequired()])
    submit = SubmitField('Transcribe')
