from rest_framework.decorators import api_view
# from rest_framework.response import Response
from django.http import HttpResponse
from twilio.twiml.voice_response import VoiceResponse

# Create your views here.


@api_view(['POST'])
def answer_call(request):
    """Respond to incoming phone calls with a brief message."""
    # Start our TwiML response
    resp = VoiceResponse()
    print("hello world")
    print(resp)
    print(type(resp))

    # Read a message aloud to the caller
    resp.say("Thank you for calling! Have a great day.", voice='Polly.Amy')
    # resp.play("https://api.twilio.com/classic.mp3")
    # return str(resp)
    return HttpResponse(
        str(resp), content_type='application/xml; charset=utf-8'
    )
