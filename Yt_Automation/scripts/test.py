import os
import time
from termcolor import colored
import google.generativeai as genai
import json

movie_name = "Salaar"
script_file = 'video_script.txt'

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
if not GOOGLE_API_KEY:
  raise ValueError('GOOGLE_API_KEY environment variable is not set')

genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])

response = model.generate_content(f"Can you give me youtube video tags for the movie {movie_name}, split the tags by commas, dont use spaces, dont give anything else other than the tags seperated by commans, try to give alot of tags that will help the video to reach more people")
# cast = json.loads(response.text)
print(response.text)

# with open('cast.json', 'w') as f:
#     json.dump(cast, f)