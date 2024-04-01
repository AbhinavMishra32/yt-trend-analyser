from elevenlabs import generate, play
from elevenlabs.api.error import RateLimitError
from elevenlabs.api.error import APIError
from pydub import AudioSegment
from termcolor import colored
from elevenlabs_unleashed.src.elevenlabs_unleashed.tts import UnleashedTTS
import os
import shutil

tts = UnleashedTTS(nb_accounts=4, create_accounts_threads=1)


with open('video_script.txt', 'r') as f:
    total_chars = len(f.read())  # Calculate the total number of characters in the file
    f.seek(0)  # Move the file pointer back to the beginning of the file
    chars_read = 0  # Initialize a counter for the number of characters read
    api_key_index = 0  # Initialize the index for the api_key list
    i =0
    while True:
        try:
            i+=1
            piece_length = 1000 # Define the number of characters to read at a time
            piece = f.read(piece_length)
            if not piece:
                break
            piece = piece.decode('utf-8') if isinstance(piece, bytes) else piece  # Convert bytes to string if necessary
            chars_read += len(piece)  # Update the number of characters read

            audio = tts.speak(  # Use the current api_key
                piece,
                voice="Alice",
                model="eleven_multilingual_v2",
                save = True
            )
            os.rename(f"saves/{piece[:10]}.wav", f"saves/{i}.wav")

            print(colored(piece, 'light_green'))
            print(colored(f"Progress: {round(chars_read * 100 / total_chars, 2)}%", 'yellow'))

        except APIError as e:
            print(f"An error occurred: {e}")
            print(colored("Use Mobile Data before running the script!", 'red'))
            break

        except KeyboardInterrupt:
            print("\nKEYBOARD INTERRUPT, Combining already processed audio files...")
            num_files = len([name for name in os.listdir('saves') if os.path.isfile(os.path.join('saves', name))])
            files = [f"saves/{i}.wav" for i in range(1, num_files + 1)]
            combined = AudioSegment.from_wav(files[0])
            for file in files[1:]:
                combined += AudioSegment.from_wav(file)

            combined.export("script_audio.mp3", format="mp3")

            shutil.rmtree('saves')
            exit(0)


# Assuming that `i` is the number of audio files you have in the `saves` directory
num_files = len([name for name in os.listdir('saves') if os.path.isfile(os.path.join('saves', name))])

files = [f"saves/{i}.wav" for i in range(1, num_files + 1)]
combined = AudioSegment.from_wav(files[0])
for file in files[1:]:
    combined += AudioSegment.from_wav(file)

combined.export("script_audio.mp3", format="mp3")

shutil.rmtree('saves')
print("Audio Created!")