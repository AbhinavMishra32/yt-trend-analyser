from elevenlabs import generate, play

audio = generate(
  api_key="3f12eb2b53e2a8a5ad0dd7be0624f9d9", #(Defaults to os.getenv(ELEVEN_API_KEY))
  text="शैतान 2024: रोमांच का शिकार या बुरे सपने का शिकंजा? (लगभग 10 मिनट)",
  voice="Rachel",
  model="eleven_multilingual_v2"
)

play(audio)