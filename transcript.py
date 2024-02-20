
from kernel.http.serialize.media import unserialize_file_fields
from typing import Dict
from django.conf import settings

import requests
import os
import json

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
        self.path_file_audio = unserialize_file_fields(None, audio_file)
        print (self.path_file_audio * 1000 )

    def server_url(self, path: str) -> str:
        """
        Returns the server URL.
        Args:
            path: The path to the server
        """
        if not settings.PRODUCTION:
            return os.path.join(settings.TEST_TRANSCRIPT_SERVER_URL, path)
        return os.path.join(settings.AWS_IA_SERVER_URL, path)

    def get_transcript(self) -> Dict:
        """Returns transcript in text format from audio file."""
        if not settings.PRODUCTION:
            return self.__request_transcript_to_server()
        return self.__request_transcript_to_aws()

    def __request_transcript_to_aws(self) -> Dict:
        file = { 'file': self.audio_file }
        response = requests.get(url=settings.AWS_IA_SERVER_URL + "/transcript", json=file)
        if response.status_code != 200:
            return { 'text': 'Transcription failed' }
        return { 'text': response.json()['data'] }
    
    def __request_transcript_to_server(self) -> Dict:
        """
        Send attachment file to server to get the transcript.
        """
        with open(self.path_file_audio, 'rb') as file:
            files = {'file': (file.name, file)}
            response = requests.post(self.server_url('transcript'), files=files)
            error = { 'text': 'Transcription failed' }

            try: 
                content = response.content.json()
            except:
                return error
            
            if content['success']:
                return { 'text': content['text'] }
            return error
        
    def get_subtitles(self) -> Dict:
        """
        Returns subtitle VTT file URL and associated language.
        """
        if not settings.PRODUCTION:
            return self.__request_subtitles_to_server()
        return self.__request_subtitles_to_aws()

    def __request_subtitles_to_server(self) -> Dict:
        """
        Send attachment file to server to get the subtitles.
        """
        with open(self.path_file_audio, 'rb') as file:
            files = {'file': (file.name, file)}
            response = requests.post(self.server_url('subtitles'), files=files)
            error = { 'text': 'Subtitles failed' }

            try: 
                content = response.content.json()
            except:
                return error
            
            if content['success']:
                return { 'text': content['text'] }
            return error

    def __request_subtitles_to_aws(self) -> Dict:
        """
        Returns subtitle VTT file URL and associated language.
        """
        file = { 
            'file': self.audio_file 
        }
        response = requests.get(url=settings.AWS_IA_SERVER_URL + "/subtitles", json=file)

        if response.status_code != 200:
            return None
        return response.json()