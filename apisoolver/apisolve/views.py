# from django.shortcuts import render
import requests
# Note: you need to be using OpenAI Python v0.27.0 for the code below to work
import openai
from icecream import ic
import json
from rest_framework.decorators import api_view
from django.http import HttpResponse
import twilio.rest
import os
from dotenv import load_dotenv
# from django.conf import settings as conf_settings
# OAKEY=conf_settings.OAKEY
dotenv_path = os.path.join(os.path.dirname(__file__), '../.env')
ic(dotenv_path)
load_dotenv(dotenv_path)
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

OAKEY=os.environ.get("OAKEY")

openai.api_key = OAKEY
asid=os.environ.get("asid")
atoken=os.environ.get("auth_token")
# client = twilio.rest.Client()
ic(asid,atoken)
client = twilio.rest.Client(asid, atoken)


def transcribe():

    audio_file = open("/media/naman/7FFD-CD8E/excrclr/Hackathons/sih23/grievance-solver/apisoolver/apisolve/abc3.mp3", "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    print("I AM HERE")
    print(transcript)


@api_view(['POST'])
def parse_unstructured_text(request):
    input_text=request.POST.get('data')
    ic(input_text)
    # print(request)
    # ic(input)
    prompt = f"""
            Following text is a transcript of a call recording from a client who wants to file a complaint which can be lodged to
            either electricity or water department of the caller's state government.

            from the text given below, extract the following fields and parse it into a json.
            
            Input transcript: {input_text}
            
            Fields:
            - client_name
            - department in which complaint is to be lodged
            - brief description of complaint
            - address (dict of full address, city, state)
            - adhaar card number (12 digits)
            
            Valid JSON Output, omit fields that are not present:
              """
    messages=[{"role": "system","content":prompt}]

    response = openai.ChatCompletion.create(
      					model="gpt-3.5-turbo", 
      					messages=messages, 
      					temperature=0, 
      					max_tokens=3000,
                        top_p=1, 
      					frequency_penalty=0, 
      					presence_penalty=0
    				)
    print(response)

    try:
        j = json.loads(response["choices"][0]["message"]["content"])
    except json.decoder.JSONDecodeError:
        j = None
        
    # out = {"prompt": prompt, "output": response["choices"][0]["message"], "json": j, "response": response}
    ic(j,type(j))
    return HttpResponse(json.dumps(j), content_type="application/json")

@api_view(['POST'])
def get_recording_url(request):
    r_url=request.POST.get('url')
    ic(r_url)
    requests.get(r_url)
