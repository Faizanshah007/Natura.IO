'''
import speech_recognition as sr

r = sr.Recognizer()

with sr.Microphone() as source:
    while(True):
        print("SAY SOMETHING");
        audio = r.listen(source)
        print("PROCESSING...PLS WAIT, THANKS")

        try:
            print("TEXT: "+r.recognize_wit(audio, key = ""));
            
        except Exception as e:
            print("Fail -", e)
'''

'''from pocketsphinx import LiveSpeech
for phrase in LiveSpeech(): print(phrase)'''


#from wit import Wit
import record_mic_voice
import threading, time


#client = Wit("")


from google.cloud import speech_v1
from google.cloud.speech_v1 import enums
import io


def sample_recognize(local_file_path):
    """
    Transcribe a short audio file using synchronous speech recognition

    Args:
      local_file_path Path to local audio file, e.g. /path/audio.wav
    """

    client = speech_v1.SpeechClient()

    # local_file_path = 'resources/brooklyn_bridge.raw'

    # The language of the supplied audio
    language_code = "en-IN"

    # Sample rate in Hertz of the audio data sent
    ##sample_rate_hertz = 16000

    # Encoding of audio data sent. This sample sets this explicitly.
    # This field is optional for FLAC and WAV audio formats.
    encoding = enums.RecognitionConfig.AudioEncoding.LINEAR16
    config = {
        "language_code": language_code,
        ##"sample_rate_hertz": sample_rate_hertz,
        "encoding": encoding,
        "speech_contexts": [{ ##Add numbers(1,two...) via class##
            "phrases":["$OPERAND",
                       "red $OPERAND right",
                       "blue $OPERAND steps left",
                       "red","green","gold","golden","yellow","blue",
                       "translate","move","shift",
                       "rotate","turn",
                       "up","upwards","north","upward","northwards","northward","above",
                       "down","south","downwards","downward","southward","southwards","below",
                       "right","east","rightward","rightwards","eastwards","eastward",
                       "left","leftward","west","leftwards","westwards","westward",
                       "all","every","extreme","top","bottom","rightmost","leftmost",
                       "move green stick by 3 units upwards.",
                       "rotate the red line.",
                       "move the red line down by 5 units.",
                       "move blue line rightwards by 3 units",
                       "move the yellow line rightwards by 5 units and the green line downwards by 6 units.",
                       "move green line towards left by 4 units.",
                       "move red line 4 unit rightwards and 2 units downwards.",
                       "rotate the golden line.",
                       "move golden line by 3 blocks towards left and then 1 block downwards",
                       "move golden stick leftwards by 2 units.",
                       "move blue line rightwards by 3 units.",
                       "move golden line by 3 blocks towards left and red line by 5 blocks towards right.",
                       "rotate the red and the green line.",
                       "move red line down by 1 unit.",
                       "move yellow line leftwards by 10 units.",
                       "move red line rightwards by 1 and then upwards by 1.",
                       "move golden line rightwards by 5 units and green line by 3 units.",
                       "move blue line 7 units southwards and then 4 units leftwards.",
                       "move the red line by 5 units towards north.",
                       "quit",
                       "move golden line down by one unit.",
                       "move the red line towards north by 5 units.",
                       "translate green line 7 units towards east and then move it up by one unit.",
                       "move yellow line down by 1 unit.",
                       "move blue line upwards by one unit and then left by one unit.",
                       "hi",
                       "rotate the blue line.",
                       "turn the red line.",
                       "move green line up by 2 units.",
                       "red move down 6 steps",
                       "move yellow up",
                       "exit",
                       "move green below and then move left 11 steps",
                       "move yellow down and repeat",
                       "move red up three",
                       "move red and green stick up by one block",
                       "move blue down",
                       "move yellow stick towards right by 2 blocks",
                       "move red left",
                       "blue left one",
                       "rotate blue stick",
                       "move left 12 steps yellow",
                       "move yellow to left",
                       "move red left seven steps",
                       "move red to top",
                       "move the blue stick one step in left",
                       "turn green right",
                       "move red stick down by 4 and then left by 1",
                       "move down green",
                       "blue move left",
                       "move the blue line to the top",
                       "move gold line to top",
                       "move green up",
                       "move yellow left",
                       "left move blue",
                       "move blue up by 5",
                       "move green to top",
                       "rotate red 90 degree",
                       "rotate green",
                       "move red right and repeat",
                       "move blue stick towards right by 8 blocks",
                       "red move seven steps left",
                       "move green left",
                       "move yellow stick towards the left by 4 blocks",
                       "move blue line left",
                       "move gold right",
                       "move green stick towards the right by 3 blocks",
                       "rotate 90 degree green",
                       "move red lefrt seven steps",
                       "repeat last",
                       "move red right three steps",
                       "move yellow down",
                       "move the green light to the top",
                       "move red stick towards the right by 1 blocks",
                       "repeat",
                       "move blue up 6 steps then move blue left 10 steps",
                       "move the green stick 7 blocks rightwards and then one block upwards.",
                       "move blue to top",
                       "quit"
                       "move yellow stick towards the right by 2 blocks",
                       "move yellow stick towards left by 3",
                       "rotate yellow",
                       "rotate yellow 90 degree",
                       "rotate blue 90 degree",
                       "move blue right",
                       "move red right",
                       "rotate 90 degree yellow",
                       "close"
                       ]
            }]
    }
    with io.open(local_file_path, "rb") as f:
        content = f.read()
    audio = {"content": content}

    response = client.recognize(config, audio)
    for result in response.results:
        # First alternative is the most probable result
        alternative = result.alternatives[0]
        print(u"Transcript: {}".format(alternative.transcript))
        while(True):
            try:
                with open('command.txt','a') as f:
                    f.write(str(alternative.transcript)+'\n')
                    f.close()
                    break
            except:
                pass

        
def f():
    global resp
    while(record_mic_voice.flag != 'stop'):
        record_mic_voice.record_to_file('command.wav')
        #with open('command.wav', 'rb') as f:
        try:
            #resp = client.speech(f, None, {'Content-Type': 'audio/wav'})
            sample_recognize('command.wav')
        except:
            pass
        #f.close()

        '''if(not str(resp['_text']).isspace()):
            with open('command.txt', 'a') as f:
                f.write(str(resp['_text']) + '\n')

                f.close()'''

thrd = threading.Thread(target = f)

def run():
    thrd.start()
