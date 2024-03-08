import pathlib
import textwrap
import json
import os
import google.generativeai as genai
from pprint import pprint
# from dotenv import load_dotenv

from IPython.display import display
from IPython.display import Markdown

# load_dotenv()

def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
if not GOOGLE_API_KEY:
  raise ValueError('GOOGLE_API_KEY environment variable is not set')

genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])

# Load video data from JSON file
ai_data = []
with open('video_data.json', 'r') as file:
    yt_data = json.load(file)
    for channel_id, channel_data in yt_data.items():
        subscriber_count = channel_data['subscriber_count']
        videos = channel_data['video']
        for video in videos:
            video_title = video["title"]
            channel_name = video["channel_name"]
            # video_link = f"https://www.youtube.com/watch?v={video['videoId']}"  # Construct YouTube video link
            video_data = {
                "channel_id": channel_id,
                "title": video_title,
                "viewCount": video["viewCount"],
                "channel_name": channel_name,
                "subscriber_count": subscriber_count,
                "video_link": video["video_link"]  # Include video link
            }
            ai_data.append(video_data)

# Print processed video data
pprint(ai_data, indent=4)

# Generate content using the processed video data
response1 = model.generate_content("I'm interested in channels that consistently upload content quickly and receive high views, indicating they likely earn substantial revenue. If a channel targets a specific niche, please mention that. Famous or well-known channels can be disregarded, as they're likely genuine. However, if a lesser-known channel with a low subscriber count is still achieving high views, please highlight it and mention the niche it targets. Additionally, for each channel, discuss the difficulty of producing their content and the challenges they may face in video production by looking at the video title. also tell the numerical data without hallucinating for each channel which isnt well known, dont tell well knwon channels by looking at the sub count!, also give youtube video links too that was viral for that channel and the video type you are suggesting can be profitable/viral/easy to make and make revenue off of." + str(ai_data))
print(response1.text)
print("-------------------")
response = model.generate_content("now with this data which channel should i create that can generate some profit with easy to produce videos that can we made in bulk" + response1.text)
print(response.text)