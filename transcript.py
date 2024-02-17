
from typing import Dict
from django.conf import settings
import requests
import os

class Transcript:
    """
    Init Object that creates transcript and summaries from audio files.

    :param audio_file: The audio file
    :type audio_file: str
    """

    def __init__(self, audio_file: str) -> None:
        """Init function.

        @param audio_file : The audio filename
        """
        self.audio_file = audio_file

    def server_url(self, path: str) -> str:
        """
        Returns the server URL.
        Args:
            path: The path to the server
        """
        if settings.DEBUG:
            return os.path.join(settings.TEST_TRANSCRIPT_SERVER_URL, path)
        return os.path.join(settings.AWS_IA_SERVER_URL, path)

    def get_transcript(self) -> Dict:
        """Returns transcript in text format from audio file."""
        file = { 'file': self.audio_file }
        response = requests.get(url=settings.AWS_IA_SERVER_URL + "/transcript", json=file)
        if response.status_code != 200:
            return { 'text': 'Transcription failed' }
        return { 'text': response.json()['data'] }

    def get_subtitles(self) -> Dict:
        """Returns subtitle VTT file URL and associated language."""

        file = { 
            'file': self.audio_file 
        }

        response = requests.get(url=settings.AWS_IA_SERVER_URL + "/subtitles", json=file)

        if response.status_code != 200:
            return None
        return response.json()