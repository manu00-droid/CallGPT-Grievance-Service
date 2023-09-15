from rest_framework.decorators import api_view
from django.http import HttpResponse
from twilio.twiml.voice_response import VoiceResponse
import twilio.rest
import requests
from django.http import JsonResponse

asid = "ACc773938691c59d16d13b0b8dacb3d461"
auth = "51a05de4dac2fc81dc56d51432bbc641"
client = twilio.rest.Client(asid, auth)


@api_view(['POST'])
def answer_call(request):

    resp = VoiceResponse()
    resp.say("Thank you for calling! Please leave your message after the tone and press 9 to end the call.")
    resp.record(
        action='/handle-recording',
        method='POST',
        maxLength='180',
        timeout='5',
        finishOnKey='9'
    )

    return HttpResponse(
        str(resp), content_type='application/xml; charset=utf-8'
    )


@api_view(['POST'])
def handle_recording(request):
    recording_url = request.POST.get("RecordingUrl")

    resp = VoiceResponse()

    if recording_url:
        resp.say("Thank you for your message. The recording has been received.")
    else:
        resp.say("No recording received.")

    return HttpResponse(
        str(resp), content_type='application/xml; charset=utf-8'
    )
