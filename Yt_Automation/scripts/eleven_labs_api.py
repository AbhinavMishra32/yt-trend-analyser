"""
This script uses the Eleven Labs API to generate audio from a text script. 
The script is read from a file and sent to the API in chunks. 
The audio responses are concatenated and saved to a file. 
The API keys are read from a text file and rotated to avoid rate limiting.
"""

from elevenlabs import generate, play
from elevenlabs.api.error import RateLimitError
from elevenlabs.api.error import APIError
from pydub import AudioSegment
import io
from termcolor import colored
from elevenlabs_unleashed.src.elevenlabs_unleashed.tts import UnleashedTTS

api_keys = []  # List to store the API keys
tts = UnleashedTTS(nb_accounts=2, create_accounts_threads=1)
# Read the API keys from the text file
with open('scripts/api_keys.txt', 'r') as f:
    api_keys = [line.strip() for line in f.readlines()]

main_audio = AudioSegment.empty()  # Initialize an empty audio segment

with open('video_script.txt', 'r') as f:
    total_chars = len(f.read())  # Calculate the total number of characters in the file
    f.seek(0)  # Move the file pointer back to the beginning of the file
    chars_read = 0  # Initialize a counter for the number of characters read
    api_key_index = 0  # Initialize the index for the api_key list
    while True:
        piece_length = 1000
        piece = f.read(piece_length)
        if not piece:
            break
        piece = piece.decode('utf-8') if isinstance(piece, bytes) else piece  # Convert bytes to string if necessary
        chars_read += len(piece)  # Update the number of characters read

        try:
            # audio = generate(
            #     api_key=api_keys[api_key_index],  # Use the current api_key
            #     text=piece,
            #     voice="Alice",
            #     model="eleven_multilingual_v2"
            # )
            audio = tts.speak(  # Use the current api_key
                piece,
                voice="Alice",
                model="eleven_multilingual_v2",
                save = True
            )
        except RateLimitError as e:
            print("Rate limit exceeded. Switching to another API key...")
            api_keys[api_key_index] = "exhausted:" + api_keys[api_key_index]  # Mark the key as exhausted
            # Open the file in append mode and write the exhausted key
            # with open('scripts/api_keys.txt', 'a') as key_file:
            #     key_file.write("exhausted:" + api_keys[api_key_index] + "\n")
            api_key_index = (api_key_index + 1) % len(api_keys)  # Switch to the next api_key
            continue

        except APIError as e:
            print(f"An error occurred: {e}")
            print(colored("Use Mobile Data before running the script!", 'red'))
            break

        main_audio += AudioSegment.from_mp3(io.BytesIO(audio))  # Concatenate the audio segments

        print(colored(piece, 'light_green'))
        print(colored(f"Progress: {round(chars_read * 100 / total_chars, 2)}%", 'yellow'))

# Export the concatenated audio to an MP3 file
main_audio.export('script_audio.mp3', format='mp3')
