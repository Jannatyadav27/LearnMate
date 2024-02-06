import requests

class GenerateVoice:
    def __init__(self, api):
        self.url = "https://api.elevenlabs.io/v1/text-to-speech/21m00Tcm4TlvDq8ikWAM"
        self.headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": api
        }

    def convert_text_to_speech(self, text, output_file='output.mp3', chunk_size=1024):
        model_id = "eleven_monolingual_v1"
        
        voice_settings = {
            "stability": 0.5,
            "similarity_boost": 0.5
        }
        
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
    from dotenv import load_dotenv
    load_dotenv()
    import os 

    ELEVEN_LABS_API = os.environ.get('ELEVEN_LABS_API')

    api = GenerateVoice(ELEVEN_LABS_API)
    text = "Born and raised in the charming south, I can add a touch of sweet southern hospitality to your audiobooks and podcasts"
    api.convert_text_to_speech(text, "static/audio/output.mp3")

