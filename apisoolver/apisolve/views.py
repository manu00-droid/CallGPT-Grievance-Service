
import requests

import openai
from icecream import ic
import json
from rest_framework.decorators import api_view
from django.http import HttpResponse
from requests.auth import HTTPBasicAuth
import datetime as dt
import twilio.rest
import os
from dotenv import load_dotenv


dotenv_path = os.path.join(os.path.dirname(__file__), '../.env')
ic(dotenv_path)
load_dotenv(dotenv_path)

OAKEY=os.environ.get("OAKEY")

openai.api_key = OAKEY
asid=os.environ.get("asid")
atoken=os.environ.get("auth_token")
message_url=os.environ.get("message_url")
DBURL=os.environ.get("DBURL")

ic(asid,atoken)
client = twilio.rest.Client(asid, atoken)

def transcribe(path,pno):
    # path=request.POST.get('url')
    audio_file = open(path, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    # print("I AM HERE")
    print(transcript)
    parse_unstructured_text(transcript,pno)




def parse_unstructured_text(transcript,phone_number):
    input_text=transcript
    ic(input_text)
    
    
    prompt = f"""
            Following text is a transcript of a call recording from a client who wants to file a complaint which can be lodged to
            either electricity or water department of the caller's state government.
            and also given a phone number, add it to the json as well.
            from the text given below, extract the following fields , and parse it into a json, after converting them to english alphabets.
            
            Input transcript: {input_text}
            phone Number:{phone_number}
            
            Fields:
            - client_name
            - department (in which complaint is to be lodged)
            - complaint_description(brief description of complaint)
            - full_address
            - city
            - state
            - pincode(if available)))
            - adhaar_card_number (12 digits)
            - phone_number (10 digits)
            - language (used by caller)
            
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
    headers={
        'content_type':"application/json"
    }
    
    ic(j,type(j),json.dumps(j))
    requests.post(DBURL,j,headers=headers)
    ic("json sent to db")
    return HttpResponse()





save_directory = "./recordings"
if not os.path.exists(save_directory):
    os.makedirs(save_directory)

@api_view(['POST'])
def get_recording_url(request):
    r_url=request.POST.get('url')
    m_no=request.POST.get('phone_no')
    ic(r_url)
    now=dt.datetime.now()
    output_directory = "../recordings"

    formatted_now = now.strftime("%Y%m%d%H%M%S")

# Ensure the output directory exists; create it if not
    os.makedirs(output_directory, exist_ok=True)

    # Specify the output file path within the directory
    output_file = os.path.join(output_directory, f"{formatted_now}.mp3")

    # Send an HTTP GET request with authentication
    response = requests.get(r_url, auth=HTTPBasicAuth(asid, atoken))

    # Check if the request was successful (HTTP status code 200)
    if response.status_code == 200:
        # Save the audio content to the specified file path
        with open(output_file, "wb") as file:
            file.write(response.content)
        print(f"Audio file downloaded and saved as {output_file}")
    else:
        print(f"Failed to download audio. HTTP status code: {response.status_code}")

    transcribe(output_file, m_no)
    os.remove(output_file)

    return HttpResponse()



@api_view(['POST'])
def translate(request):
    j=request.POST
    text=f"Hi {j['name']}, your complaint has been registered with the {j['department']} department, with complaint id {j['cid']}. Here is the description of your complaint:\n {j['complaintDescription']}"
    prompt = f"""
            Following text is a data of the Name of a person,his phone number,  and a Complaint-ID, also a language is given,the department of the complain, and a brief complaint description. 

            Translate the data into the language specified in the text, and return the translation as text with the same structure as before, just change the language.
            
            Input text: {text}
            Language to be chages into : {j['language']}
            
            Valid text Output:
              """
    messages=[{"role": "system","content":prompt}]

    # response = openai.ChatCompletion.create(
    #   					model="gpt-3.5-turbo", 
    #   					messages=messages, 
    #   					temperature=0, 
    #   					max_tokens=3000,
    #                     top_p=1, 
    #   					frequency_penalty=0, 
    #   					presence_penalty=0
    				# )
    # print(response)

    # try:
    #     k = json.loads(response["choices"][0]["message"]["content"])
    # except json.decoder.JSONDecodeError:
    #     k=None
    k=text
    print(k)

    phno=j['phoneNumber']
    req_body={
        "phone_no":phno,
        "body":k
    }
    requests.post(message_url,req_body)
    return HttpResponse()

