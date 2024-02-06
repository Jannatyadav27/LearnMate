import requests

class SearchStockVideo:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.gettyimages.com/v3/search/videos"

    def search_videos(self, topic, num_videos=1):
        headers = {
            'Api-Key': self.api_key,
        }

        params = {
            'phrase': topic,
            'page_size': num_videos,
        }

        response = requests.get(self.base_url, headers=headers, params=params)

        if response.status_code == 200:
            videos = response.json().get('videos', [])
            return videos
        else:
            print(f"Error: {response.status_code}")
            return None

# Example usage:
if __name__ == "__main__":
    api_key = 'YOUR_API_KEY'
    
    getty_media_api = SearchStockVideo(api_key)
    topic = 'photosynthesis'
    result = getty_media_api.search_videos(topic, num_videos=1)

    if result:
        if result:
            print("Stock Video Information:")
            print("Title:", result[0].get('title', 'N/A'))
            print("Preview URL:", result[0].get('display_sizes', [{}])[0].get('uri', 'N/A'))
        else:
            print("No stock videos found.")
