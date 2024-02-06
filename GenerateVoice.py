import requests

class TextToSpeechAPI:
    def __init__(self, url, headers):
        self.url = url
        self.headers = headers

    def convert_text_to_speech(self, text, model_id, voice_settings, output_file='output.mp3', chunk_size=1024):
        data = {
            "text": text,
            "model_id": model_id,
            "voice_settings": voice_settings
        }

        try:
            response = requests.post(self.url, json=data, headers=self.headers)
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx status codes)

            with open(output_file, 'wb') as f:
                for chunk in response.iter_content(chunk_size=chunk_size):
                    if chunk:
                        f.write(chunk)
            print("Audio file saved successfully.")
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    url = "https://api.elevenlabs.io/v1/text-to-speech/21m00Tcm4TlvDq8ikWAM"
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": "d6a1adbbd3c0060cf386d4689610c1b3"
    }

    api = TextToSpeechAPI(url, headers)

    text = "Born and raised in the charming south, I can add a touch of sweet southern hospitality to your audiobooks and podcasts"
    model_id = "eleven_monolingual_v1"
    voice_settings = {
        "stability": 0.5,
        "similarity_boost": 0.5
    }

    api.convert_text_to_speech(text, model_id, voice_settings)

