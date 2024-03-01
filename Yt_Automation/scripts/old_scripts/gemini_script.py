import google.generativeai as genai
import os
from termcolor import colored

movie_name = "Crakk 2024"

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
if not GOOGLE_API_KEY:
  raise ValueError('GOOGLE_API_KEY environment variable is not set')

genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])

# Start the script
response = model.generate_content(f"can you write about the movie {movie_name},This will be the script for a YouTube video that tells about the movie and how its being received by the people, and tell in general what happens in the movie and about actors and actresses's experiences while filming, write about the rating of the movie if available, and also write the previous works of the actors which are inside of this movie, talk in detail about everything. write it in hindi, also write theintro to the video by telling to like and subscribe the channel for more content, and add your own things as well to say to improve viewer retention. stop until you can write, dont end the script as I will ask to continue the script in the next request., make the script as long as possible upto 10 minutes of video, your max output of the script should be 10 minutes of video!, make the script continuous, dont add titles!!! DONT ADD TITLES AND HEADINGS TO THE SCRIPT! AND DONT HAVE POINTS, LET IT BE A CONTINOUS SCRIPT!")
with open('video_script.txt', 'w') as f:
    f.write(response.text)

# Continue the script
for _ in range(4):  # Adjust this number based on how many times you want to continue the script
    print("Iteration:", _)
    last_part = response.text.split()[-100:]  # Get the last 100 words from the response
    last_part = ' '.join(last_part)
    response = model.generate_content(f"continue the script from the previous request, stop until you can write, dont end the script as I will ask to continue the script in the next request., make the script as long as possible!, please! its for my youtube video, please give me a long script, as long as you can keep going! , IMPORTANT NOTE: DONT MAKE IT POINT BASED, NOR HAVE HEADINGS OR ANYTHING ELSE LIKE THAT, JUST MAKE IT CONTINOUS AS AN ESSAY TYPE, if you see repeating words then quickly break that and start making realistic text again! (please) The script: {last_part[-800:]}")
    print(f"-----------RESPONSE {_}-----------")
    print(response.text)
    # response = model.generate_content(f"continue the script from the previous request, stop until you can write, dont end the script as I will ask to continue the script in the next request., make the script as long as possible!, please! its for my youtube video, please give me a long script, as long as you can keep going! , IMPORTANT NOTE: DONT MAKE IT POINT BASED, NOR HAVE HEADINGS OR ANYTHING ELSE LIKE THAT, JUST MAKE IT CONTINOUS AS AN ESSAY TYPE")

    with open('video_script.txt', 'a') as f:
        f.write(response.text)
        colored((f"appended response {_} to file"), 'green')

# Finish the script with an outro
response = model.generate_content(f"Continue this script, and now stop with an outro of the channel., make the script as long as possible! The script: {last_part[-800:]}")
# response = model.generate_content(f"Continue this script, and now stop with an outro of the channel., make the script as long as possible!")

with open('video_script.txt', 'a') as f:
    f.write(response.text)
