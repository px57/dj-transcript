
from transcript.transcript import Transcript
from kernel.http import Response

def transcript(request):
    """
    Transcribe an audio file.

    :param request: The request object.
    :type request: Request

    :return: The response object.
    :rtype: Response
    """
    res = Response()
    # -> Get the audio file from the request. 
    # -> and send to the AWS_IA_SERVER_URL for transcription. 
    return res.success()


def subtitles(request):
    """
    Get subtitles for an audio file.

    :param request: The request object.
    :type request: Request

    :return: The response object.
    :rtype: Response
    """
    res = Response()
    # -> Get the audio file from the request. 
    # -> and send to the AWS_IA_SERVER_URL for subtitles. 
    return res.success()