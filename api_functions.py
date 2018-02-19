"""
There are 3 functions defiend here:
    1. splitter: getting an audio path in .wav format, splitting it into 1 minute audios in .flac format 
    and exporting them with chunk{i}.flac name
    2. speech_req: getting an audio path in .flac format, sending this audio to google cloud speech 
    and returning the text
    3. speech_recog: getting and audio path, passing it to splitter function, passing the splitted audios
    to speech_req function and passing the result to a url_path
    
Requirements:
    1. pydub 
    2. google-cloud-speech
"""


def splitter(audio_file_path):
    import os
    from pydub import AudioSegment 
    from pydub.utils import make_chunks
    
    
    name = os.path.basename(audio_file_path)
    name = name.replace(".wav","")
    myaudio = AudioSegment.from_file(audio_file_path,"wav")
    # 60000 = 1 minute
    chunk_length_ms = 60000
    chunks = make_chunks(myaudio,chunk_length_ms)
    
    for i, chunk in enumerate(chunks):
        chunk_name = (name+"_{0}.flac").format(i)
        # number of channels in flac = 1
        chunk.export(os.path.join(os.path.dirname(audio_file_path),chunk_name), format="flac", parameters = ["-ac","1"])
    return i
        
    

def speech_req(audio_file_path):
    
    import io
    import json
    
    # Imports the Google Cloud client library
    from google.cloud import speech
    # enums for specifying config
    from google.cloud.speech import enums
    from google.cloud.speech import types
    
    
    # Instantiates a client
    client = speech.SpeechClient()


    # Loads the audio into memory
    with io.open(audio_file_path, 'rb') as audio_file:
        content = audio_file.read()
        audio = types.RecognitionAudio(content=content)

    config = types.RecognitionConfig(
        language_code='fa-IR')

    # Detects speech in the audio file
    response = client.recognize(config, audio)
    
    string = ''
    conf = []

    for result in response.results:
        string+=json.dumps(result.alternatives[0].transcript, ensure_ascii=False)
        conf = result.alternatives[0].confidence

    return string, conf



def speech_recog(audio_file_path):
    
    import os
    import requests
    
    
    counter = splitter(audio_file_path)+1
    name = os.path.basename(audio_file_path)
    name = name.replace(".wav","")

    
    for i in range(0,counter):
        chunk_name = name+"_"+str(i)+".flac"
        speech_req(os.path.join(os.path.dirname(audio_file_path),chunk_name))

""""
    # sending the result to url_path
    data = {"transcript" : result, "requestId" : name, "confidence" : conf}
    requests.post(url_path, json=data)
    
    result[i], conf[i] = speech_req(os.path.join(os.path.dirname(audio_file_path),chunk_name))
            # removing double quote character from the result
        #result[i] = result[i].replace('\"',"")
    return result
    """
