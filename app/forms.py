from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class YoutubeForm(FlaskForm):
    yt_url = StringField('URLS',validators=[DataRequired()])
    submit = SubmitField('Transcribe')
    print('test')
