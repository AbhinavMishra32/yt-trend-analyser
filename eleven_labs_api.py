from elevenlabs import generate, play
from pydub import AudioSegment

with open('myfile.txt', 'r') as f:
	i = 0
	while range(0,3):
		i+=1
		piece = f.read(100)
		piece = piece.decode('utf-8') if isinstance(piece, bytes) else piece  # Convert bytes to string if necessary
		audio = generate(
			api_key="f09f5318bdd39f0a5f1ff9f2f78730c8", #(Defaults to os.getenv(ELEVEN_API_KEY))
			text=piece,
			voice="Rachel",
			model="eleven_multilingual_v2"
		)

		with open('script_audio.wav', 'wb') as f:
				f.write(audio)

		audio_segment = AudioSegment.from_wav(f'script_audio_{i}.wav')
		audio_segment.export('script_audio.mp3', format='mp3')
						
		if not piece:
			break
		print(piece)

# play(audio)