import json
from os.path import join, dirname
from ibm_watson import SpeechToTextV1
from ibm_watson.websocket import RecognizeCallback, AudioSource
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import json

authenticator = IAMAuthenticator('KJPpUcoWbORi-40RilpCkT6RsfWrmKFDKU39As0hMMOj') #api 35YeGfu8s4jpiQl_dASuqLBvgun0e5heVTgrqrBroJhG
speech_to_text = SpeechToTextV1(
    authenticator=authenticator
)

speech_to_text.set_service_url('https://api.us-south.speech-to-text.watson.cloud.ibm.com/instances/ba23ed39-9f6b-4014-bc2b-fdb0bb6dda2e')

class MyRecognizeCallback(RecognizeCallback):
    def __init__(self):
        RecognizeCallback.__init__(self)

    def on_data(self, data):
        received = json.dumps(data, indent=2) 
        print(received)

    def on_error(self, error):
        print('Error received: {}'.format(error))

    def on_inactivity_timeout(self, error):
        print('Inactivity timeout: {}'.format(error))

myRecognizeCallback = MyRecognizeCallback()

def transcribe(audio_filename):
    #with open(join(dirname(__file__), './static/', audio_file),'rb') as audio_file:
    with open(audio_filename,'rb') as audio_file:
        #audio_source = AudioSource(audio_file)
        data = speech_to_text.recognize(
            audio=audio_file,
            content_type='audio/mp3',
            speaker_labels=True,  #recognize_callback=myRecognizeCallback,
            model='en-US_BroadbandModel')
        final_data = json.loads(str(data))
        return final_data['result']