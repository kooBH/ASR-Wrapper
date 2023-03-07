# pip install --upgrade google-api-python-client
# pip install google-cloud-speech

import os,glob
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "key/google_key.json"

def transcribe_streaming(stream_file):
    print("streaming {}".format(stream_file))
    """Streams transcription of the given audio file."""
    import io
    from google.cloud import speech

    client = speech.SpeechClient()
    
    stream = []
    with io.open(stream_file, "rb") as audio_file :
        # dump header
        audio_file.read(44)
        while True : 
            content = audio_file.read(128)
            if not content:
                # eof
                break
            stream.append(content)

    requests = (
        speech.StreamingRecognizeRequest(audio_content=chunk) for chunk in stream
    )
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
    )

    streaming_config = speech.StreamingRecognitionConfig(
        config=config,
        interim_results=True
    )

    # streaming_recognize returns a generator.
    responses = client.streaming_recognize(
        config=streaming_config,
        requests=requests,
    )
    
    name_file = stream_file.split("\\")[-1]
    id_file = name_file.split(".")[0]
    with open("output/{}_stream.txt".format(id_file),"w") as f : 
        for response in responses:
            # Once the transcription has settled, the first result will contain the
            # is_final result. The other results will be for subsequent portions of
            # the audio.
            for result in response.results:
                #print("{} ".format(result.is_final),end = "")
                #print("{:.2f}:".format(result.stability),end = "")
                alternatives = result.alternatives
                # best only
                f.write(u"{}| ".format(alternatives[0].transcript))
                print(u"{}| ".format(alternatives[0].transcript),end = "")
                #print("||",end = "")
            f.write("\n")
            print("")

def transcribe_file(speech_file):
    print("file {}".format(speech_file))
    """Transcribe the given audio file."""
    from google.cloud import speech
    import io

    client = speech.SpeechClient()

    with io.open(speech_file, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
    )

    response = client.recognize(config=config, audio=audio)
    name_file = speech_file.split("\\")[-1]
    id_file = name_file.split(".")[0]
    with open("output/{}_file.txt".format(id_file),"w") as f : 
        # Each result is for a consecutive portion of the audio. Iterate through
        # them to get the transcripts for the entire audio file.
        for result in response.results:
            # The first alternative is the most likely one for this portion.
            f.write(u"{}".format(result.alternatives[0].transcript))
            print(u"{}".format(result.alternatives[0].transcript))
        f.write("\n")


if __name__ == "__main__": 
    list_target = glob.glob(os.path.join("data","Disney_test_streaming_ch","*.wav"))
    print(len(list_target))
    for path in list_target : 
        transcribe_streaming(path)
        transcribe_file(path)