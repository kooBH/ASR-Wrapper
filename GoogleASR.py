# pip install --upgrade google-api-python-client
# pip install google-cloud-speech

import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "key/google_key.json"

def transcribe_streaming(stream_file):
    print("transcribe_streaming")
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

    for response in responses:
        # Once the transcription has settled, the first result will contain the
        # is_final result. The other results will be for subsequent portions of
        # the audio.
        for result in response.results:
            print("{} ".format(result.is_final),end = "")
            print("{:.2f}:".format(result.stability),end = "")
            alternatives = result.alternatives
            # The alternatives are ordered from most likely to least.
            for i, alternative in enumerate(alternatives):
                print(u"{}|".format(alternative.transcript),end = "")
            print("||",end = "")
        print("")

def transcribe_file(speech_file):
    print("transcribe_file")
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

    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    for result in response.results:
        # The first alternative is the most likely one for this portion.
        print("Transcript: {}".format(result.alternatives[0].transcript))


if __name__ == "__main__": 
    path = "data/F01_050C0103_BUS_clean.wav"
    print(path)
    transcribe_streaming(path)
    transcribe_file(path)