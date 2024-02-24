
from django.conf import settings
from kernel.http.serialize.media import serialize_file_fields
from transcript.transcript import Transcript
from kernel.http import Response
# csrf_exempt
from django.views.decorators.csrf import csrf_exempt
from uuid import uuid4
import os

def media_save(file):
    """
    Save the file in the media folder.
    Args:
        file: The file to save in the media folder.
    """
    file_name = str(uuid4()) + file.name
    transcript_path = os.path.join(settings.MEDIA_ROOT, 'transcripts')
    if not os.path.exists(transcript_path):
        os.makedirs(transcript_path)

    path = os.path.join(transcript_path, file_name)
    with open(path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    return path

def generate_url(path):
    """
    Generate the URL for the file.
    Args:
        path: The path to the file.
    """
    path = path.replace(settings.MEDIA_ROOT, '')
    url = settings.ADRESS_HOST + settings.MEDIA_URL + path
    return url

@csrf_exempt
def transcript(request):
    """
    Transcribe an audio file.

    :param request: The request object.
    :type request: Request

    :return: The response object.
    :rtype: Response
    """
    res = Response()
    audio_file = request.FILES['file']
    audio_file_name = media_save(audio_file)
    
    transcript = Transcript(generate_url(audio_file_name))
    result = transcript.get_transcript()
    res.result = result
    print ("------------------------------------------->>>>")
    print (res.result)
    return res.success()

@csrf_exempt
def subtitles(request):
    """
    Get subtitles for an audio file.

    :param request: The request object.
    :type request: Request

    :return: The response object.
    :rtype: Response
    """
    res = Response()
    audio_file = request.FILES['file']
    audio_file_name = media_save(audio_file)

    transcript = Transcript(generate_url(audio_file_name))
    result = transcript.get_subtitles()
    res.result = result
    print ("------------------------------------------->>>>")
    print (res.result)
    return res.success()