import requests
from requests.auth import HTTPBasicAuth
import os

# Replace these with your actual URL, username, and password
url = "https://api.twilio.com/2010-04-01/Accounts/ACc773938691c59d16d13b0b8dacb3d461/Recordings/RE5756c07eb3838fc0f8d09acbf8205dce"
username = "ACc773938691c59d16d13b0b8dacb3d461"
password = "11bcd25e313567df199e7ab5de35c437"

# Define the directory path where you want to save the downloaded audio file
output_directory = "../recordings"

# Ensure the output directory exists; create it if not
os.makedirs(output_directory, exist_ok=True)

# Specify the output file path within the directory
output_file = os.path.join(output_directory, "downloaded_audio.mp3")

# Send an HTTP GET request with authentication
response = requests.get(url, auth=HTTPBasicAuth(username, password))

# Check if the request was successful (HTTP status code 200)
if response.status_code == 200:
    # Save the audio content to the specified file path
    with open(output_file, "wb") as file:
        file.write(response.content)
    print(f"Audio file downloaded and saved as {output_file}")
else:
    print(f"Failed to download audio. HTTP status code: {response.status_code}")
