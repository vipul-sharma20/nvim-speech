import os
import queue

import pyaudio
from vernacular.ai import speech
from vernacular.ai.speech import enums, types

RATE = 8000
CHUNK = int(RATE / 10)  # 100ms


class MicrophoneStream(object):
    """Opens a recording stream as a generator yielding the audio chunks."""

    def __init__(self, rate, chunk):
        self._rate = rate
        self._chunk = chunk

        # Create a thread-safe buffer of audio data
        self._buff = queue.Queue()
        self.closed = True
        self.file = open("audio.raw", "ab")

    def __enter__(self):
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            # The API currently only supports 1-channel (mono) audio
            # https://goo.gl/z757pE
            channels=1,
            rate=self._rate,
            input=True,
            frames_per_buffer=self._chunk,
            # Run the audio stream asynchronously to fill the buffer object.
            # This is necessary so that the input device's buffer doesn't
            # overflow while the calling thread makes network requests, etc.
            stream_callback=self._fill_buffer,
        )

        self.closed = False

        return self

    def __exit__(self, type, value, traceback):
        self.end()

    def end(self):
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self.closed = True
        # Signal the generator to terminate so that the client's
        # streaming_recognize method will not block the process termination.
        self._buff.put(None)
        self._audio_interface.terminate()
        self.file.close()

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        """Continuously collect data from the audio stream, into the buffer."""
        self._buff.put(in_data)
        self.file.write(in_data)
        return None, pyaudio.paContinue

    def generator(self):
        while not self.closed:
            # Use a blocking get() to ensure there's at least one chunk of
            # data, and stop iteration if the chunk is None, indicating the
            # end of the audio stream.
            chunk = self._buff.get()
            if chunk is None:
                return
            data = [chunk]

            # Now consume whatever other data's still buffered.
            while True:
                try:
                    chunk = self._buff.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                except queue.Empty:
                    break

            yield b"".join(data)


def vernacular_asr(language_code: str) -> str:
    access_token: str = os.environ.get("VERNACULAR_ACCESS_TOKEN", "")
    transcript: str = ""

    with MicrophoneStream(RATE, CHUNK) as stream:
        client = speech.SpeechClient(access_token)
        config = types.RecognitionConfig(
            encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=RATE,
            language_code=language_code,
        )
        silence_detection_config = types.SilenceDetectionConfig(
            enable_silence_detection=True,
            max_speech_timeout=15,
            silence_patience=4.5,
            no_input_timeout=1.5,
        )
        audio_generator = stream.generator()
        requests = (
            types.StreamingRecognizeRequest(audio_content=content)
            for content in audio_generator
        )

        streaming_config = types.StreamingRecognitionConfig(
            config=config, silence_detection_config=silence_detection_config
        )

        try:
            responses = client.streaming_recognize(streaming_config, requests)

            # Now, put the transcription responses to use.
            for response in responses:
                if (
                    len(response.results) > 0
                    and len(response.results[0].alternatives) > 0
                ):
                    # Display the transcription of the top alternative.
                    transcript = response.results[0].alternatives[0].transcript
                    yield transcript
                    print(transcript)
                else:
                    print("Empty results")
        except:
            pass
        stream.end()
    return transcript


def google_asr(language_code):
    raise NotImplementedError

