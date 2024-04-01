import os
import time
from termcolor import colored
import google.generativeai as genai
import json
import sys

if len(sys.argv) < 2:
    print("Please provide the movie name as a command-line argument.")
    sys.exit(1)

movie_name = sys.argv[1]
script_file = 'video_script.txt'

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
if not GOOGLE_API_KEY:
  raise ValueError('GOOGLE_API_KEY environment variable is not set')

genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])

def write_to_script(text):
    with open(script_file, 'a') as f:
        f.write(f"{text} \n")  # Add newline character for better readability

def remove_last_response_from_script():
    with open(script_file, 'r') as f:
        lines = f.readlines()
    with open(script_file, 'w') as f:
        f.writelines(lines[:-2])  # Remove the last two lines (last AI response and newline)

def detect_repeating_text():
    with open(script_file, 'r') as f:
        script_content = f.read()
    lines = script_content.split('\n')
    last_response = lines[-2] if len(lines) > 1 else ''  # Consider last two lines for context
    repeated_text = ''
    for i in range(len(lines) - 3, -1, -1):  # Look for repetition in previous responses
        if lines[i] == last_response:
            repeated_text = last_response
            break
    return repeated_text

def generate_next_response(previous_context):
    response = model.generate_content(previous_context)
    return response.text

def handle_repeating_text():
    repeated_text = detect_repeating_text()
    if repeated_text:
        print(colored(f"Detected repeating text: {repeated_text}", 'yellow'))
        remove_last_response_from_script()
        time.sleep(3)  # Wait for a few seconds before making the next request to avoid rate limiting
        previous_context = ' '.join(response.text.split()[-500:])  # Increase context length to avoid repetition
        next_response = generate_next_response(previous_context)
        write_to_script(next_response)
        print(colored("Generated non-repeating text:", 'green'))
        print(next_response)


# Start the script
initial_context = f"can you write about the movie {movie_name} in hindi,This will be the script for a YouTube video, (so use long sentences) that tells about the movie and how its being received by the people, and tell in general what happens in the movie and about actors and actresses's experiences while filming, write about the rating of the movie if available, and also write the previous works of the actors which are inside of this movie, talk in detail about everything. write it in hindi, also write the intro to the video by telling to like and subscribe the channel for more content, important: dont use questions and answers, dont use any point based script, just let it flow continuously as an essay. Stop until you can write, dont end the script as I will ask to continue the script in the next request., make the script as long as possible upto 10 minutes of video, your max output of the script should be 10 minutes of video!, make the script continuous, dont add titles!!! DONT ADD TITLES AND HEADINGS TO THE SCRIPT! AND DONT HAVE POINTS, LET IT BE A CONTINOUS SCRIPT!"
response = model.generate_content(initial_context)

with open(script_file, 'w') as f:  # Write initial response to the script file
    f.write(response.text)

# Continue the script

for _ in range(3):  # Adjust this number based on how many times you want to continue the script
    print("Iteration:", _)
    
    # Access and store the latest script content
    with open(script_file, 'r') as f:
        last_part = f.read()

    handle_repeating_text()

    # Generate next response using the latest script content as context
    next_response = model.generate_content(f"Continue the script: {last_part}")
    write_to_script(next_response.text)

# Finish the script with an outro
handle_repeating_text()

print("----------------------")
print(colored("Script generation complete!", 'green'))
print(colored(f"Script length: {len(open(script_file).read())}", 'green', attrs=['bold']))
print("----------------------")


response = model.generate_content(f"Can you give me the description of the youtube movie {movie_name}, for a youtube video.")
with open('description.txt', 'w') as f:
    f.write(response.text)
    print(colored(f"Description: {response.text}", 'yellow'))


reponse = model.generate_content(f"Can you give me youtube video tags for the movie {movie_name}, split the tags by commas, dont use spaces, dont give anything else other than the tags seperated by commans, try to give alot of tags that will help the video to reach more people")
with open('tags.txt', 'w') as f:
    f.write(response.text)
    print(colored(f"Tags: {response.text}", 'yellow'))