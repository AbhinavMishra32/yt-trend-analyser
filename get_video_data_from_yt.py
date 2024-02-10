import requests

def search_youtube_videos(api_key, query, published_after):
    # Define the endpoint URL for the search.list method
    endpoint_url = "https://www.googleapis.com/youtube/v3/search"
    
    # Define parameters for the API request
    params = {
        'key': api_key,
        'part': 'snippet',
        'q': query,
        'order': 'viewCount',
        'type': 'video',
        'publishedAfter': published_after
    }

    # Make the API request
    response = requests.get(endpoint_url, params=params)
    response_json = response.json()

    # Extract video IDs from the search results
    videos = []
    for item in response_json['items']:
        video = {
            'video_id': item['id']['videoId'],
            'title': item['snippet']['title'],
            'published_at': item['snippet']['publishedAt'],
            'channel_id': item['snippet']['channelId']
        }
        videos.append(video)

    return videos

def get_video_statistics(api_key, video_ids):
    # Define the endpoint URL for the videos.list method
    endpoint_url = "https://www.googleapis.com/youtube/v3/videos"
    
    # Define parameters for the API request
    params = {
        'key': api_key,
        'part': 'snippet,statistics',
        'id': ','.join(video_ids)
    }

    # Make the API request
    response = requests.get(endpoint_url, params=params)
    response_json = response.json()

    # Extract relevant information for each video
    video_data = {}
    for item in response_json['items']:
        video_id = item['id']
        video_data[video_id] = {
            'title': item['snippet']['title'],
            'published_at': item['snippet']['publishedAt'],
            'channel_title': item['snippet']['channelTitle'],
            'view_count': item['statistics']['viewCount']
        }

    return video_data

def main():
    # Set your YouTube Data API key
    api_key = "AIzaSyCWCOeo2sRTa_0hB_s9RnR80dgASrjl9dY"

    # Set the title you want to search for
    query = "bollywood movies"

    # Set the date after which videos should be published (in YYYY-MM-DD format)
    published_after = "2022-01-01T00:00:00Z"

    # Call the search_youtube_videos function to search for videos
    videos = search_youtube_videos(api_key, query, published_after)

    # Extract video IDs
    video_ids = [video['video_id'] for video in videos]

    # Call the get_video_statistics function to get view counts for the videos
    video_statistics = get_video_statistics(api_key, video_ids)

    # Sort videos by view count
    sorted_videos = sorted(videos, key=lambda x: int(video_statistics[x['video_id']]['view_count']), reverse=True)

    # Display the sorted results
    for idx, video in enumerate(sorted_videos, start=1):
        video_id = video['video_id']
        title = video_statistics[video_id]['title']
        published_at = video_statistics[video_id]['published_at']
        channel_title = video_statistics[video_id]['channel_title']
        view_count = video_statistics[video_id]['view_count']
        print(f"Video {idx}:")
        print(f"Title: {title}")
        print(f"Published At: {published_at}")
        print(f"Channel: {channel_title}")
        print(f"View Count: {view_count}")
        print()

if __name__ == "__main__":
    main()
