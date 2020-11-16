import os
import sys
import json
import wave
import subprocess
from datetime import datetime

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

import pynvim
import pyaudio

from asr import vernacular_asr, google_asr


@pynvim.plugin
class Voice(object):
    def __init__(self, nvim):
        self.nvim = nvim
        self.audio = pyaudio.PyAudio()
        self.calls = 0
        self.providers = {"vernacular": vernacular_asr, "google_asr": google_asr}

    @pynvim.command("SpeechEcho", nargs="*", sync=False)
    def speech_echo_handler(self, args):
        self.speech(args, is_echo=True)

    @pynvim.command("Speech", nargs="*", sync=False)
    def speech_handler(self, args):
        self.speech(args)

    def speech(self, args, is_echo=False):
        print(self.nvim.vars)
        self.nvim.command('echo "Start speaking..."')
        transcripts = self.record_and_transcribe(args)

        for transcript in transcripts:
            if is_echo:
                self.nvim.current.line = transcript.capitalize()
            self.nvim.command(f"let g:asr_transcription='{transcript}'")
        self.nvim.command('echo "Done!"')

    def record_and_transcribe(self, args) -> str:
        try:
            provider = self.nvim.eval("g:asr_provider")
            language_code = self.nvim.eval("g:asr_language_code")
        except pynvim.api.nvim.NvimError:
            self.nvim.command(
                'echo "asr_provider and/or asr_language_code not set. Check help nvim-speech"'
            )

        return self.providers.get(provider)(language_code)

