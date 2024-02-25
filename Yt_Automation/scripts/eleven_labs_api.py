from elevenlabs import generate, play
from pydub import AudioSegment
import io

main_audio = AudioSegment.empty()  # Initialize an empty audio segment

with open('video_script.txt', 'r') as f:
    total_chars = len(f.read())  # Calculate the total number of characters in the file
    f.seek(0)  # Move the file pointer back to the beginning of the file
    chars_read = 0  # Initialize a counter for the number of characters read
    # for i in range(0,3): # for limited script
    while True: # for the entire script
        piece_length = 1000
        piece = f.read(piece_length)
        if not piece:
            break
        piece = piece.decode('utf-8') if isinstance(piece, bytes) else piece  # Convert bytes to string if necessary
        chars_read += len(piece)  # Update the number of characters read

        audio = generate(
            api_key="f09f5318bdd39f0a5f1ff9f2f78730c8", #(Defaults to os.getenv(ELEVEN_API_KEY))
            text=piece,
            voice="bd7LHIbDytVpB0tHlvAM",
            model="eleven_multilingual_v2"
        )

        # Convert the audio data to an AudioSegment without saving it to a file
        audio_file = io.BytesIO(audio) # type: ignore
        audio_segment = AudioSegment.from_mp3(audio_file)

        main_audio += audio_segment  # Concatenate the audio segments

        print(piece)
        print(f"Progress: {round(chars_read * 100 / total_chars, 2)}%")

# Export the concatenated audio to an MP3 file
main_audio.export('script_audio.mp3', format='mp3')