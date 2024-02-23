import requests

url = "https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

payload = {
    "model_id": "<string>",
    "pronunciation_dictionary_locators": [
        {
            "pronunciation_dictionary_id": "<string>",
            "version_id": "<string>"
        }
    ],
    "text": "<string>",
    "voice_settings": {
        "similarity_boost": 123,
        "stability": 123,
        "style": 123,
        "use_speaker_boost": True
    }
}
headers = {"Content-Type": "application/json"}

response = requests.request("POST", url, json=payload, headers=headers)

print(response.text)