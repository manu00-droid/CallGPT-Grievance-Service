from rest_framework.decorators import api_view
from django.http import HttpResponse
from twilio.twiml.voice_response import VoiceResponse
import twilio.rest
import requests
from django.http import JsonResponse
from dotenv import load_dotenv
import os

dotenv_path = os.path.join(os.path.dirname(__file__), '../.env')
load_dotenv(dotenv_path)
LLMURL=os.environ.get("LLMURL")

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
    print(request.POST.get("From"))
    recording_url = request.POST.get("RecordingUrl")
    phone_number = request.POST.get("From")

    resp = VoiceResponse()
    success = sendRequest(recording_url,phone_number)
    if recording_url:
        resp.say("Thank you for your message. The recording has been received.")
    else:
        resp.say("No recording received.")

    return HttpResponse(
        str(resp), content_type='application/xml; charset=utf-8'
    )


def sendRequest(url,ph_no):
    data_to_send = {
        "url": url,
        "phone_no":ph_no
    }
    response = requests.post(LLMURL , data_to_send)
    if response.status_code == 200:
        return True
    else:
        return False
    

@api_view(['POST'])
def confirm_message(request):
    print(request.POST)
    return HttpResponse("HI")

