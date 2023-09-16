from rest_framework.decorators import api_view
from django.http import HttpResponse
from twilio.twiml.voice_response import VoiceResponse
from twilio.rest import Client
import requests
from django.http import JsonResponse
from dotenv import load_dotenv
import os


dotenv_path = os.path.join(os.path.dirname(__file__), '..\.env')
load_dotenv(dotenv_path)
print(dotenv_path)
LLMURL=os.environ["LLMURL"]
asid=os.environ["asid"]
auth_token=os.environ["auth_token"]
api_key = os.environ["api_key"]
api_secret = os.environ["api_secret"]
client = Client(api_key,api_secret,asid)
# accounts = client.api.v2010.accounts.list(limit=20)
@api_view(['POST'])
def answer_call(request):

    resp = VoiceResponse()
    resp.say("Thank you for calling! Please leave your message after the tone and press 9 to end the call.",language="hi-IN")
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
    print(recording_url)
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
    body = request.POST.get("body")
    phone_no = request.POST.get("phone_no")
    message = client.messages.create(
        from_='+12569739784',
        body= body,
        to=phone_no
    )
    return HttpResponse()

    # print(message.sid)

