import google.generativeai as genai
import os

movie_name = "Deadpool 3"

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
if not GOOGLE_API_KEY:
  raise ValueError('GOOGLE_API_KEY environment variable is not set')

genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])

response1 = model.generate_content(f"can you write about the movie {movie_name},This will be the script for a YouTube video that tells about the movie and how its being received by the people, and tell in general what happens in the movie and about actors and actresses's experiences while filming, write about the rating of the movie if available, and also write the previous works of the actors which are inside of this movie, talk in detail about everything. write it in hindi, also write theintro to the video by telling to like and subscribe the channel for more content, and add your own things as well to say to improve viewer retention. stop until you can write, dont end the script as I will ask to continue the script in the next request., make the script as long as possible")
with open('video_script.txt', 'w') as f:
    f.write(response1.text)


response2 = model.generate_content(f"continue the script from the previous request, stop until you can write, dont end the script as I will ask to continue the script in the next request., make the script as long as possible!" + "The script:" + response1.text)
with open('video_script.txt', 'a') as f:
    f.write(response2.text)

with open('video_script.txt', 'r') as f:
    response_combined = f.read()

response3 = model.generate_content(f"Continue this script, and now stop with an outro of the channel., make the script as long as possible!" + "The script:" + response_combined)

with open('video_script.txt', 'a') as f:
    f.write(response3.text)

print("Script generated successfully!")
print("Please check the video_script.txt file to see the generated script.")

with open('video_script.txt', 'r') as f:
    script = f.read()
    print(script)