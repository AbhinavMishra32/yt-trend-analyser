import os
import re
import googleapiclient.discovery
from pytube import YouTube
import requests

def sanitize_filename(filename):
    # Replace invalid characters with underscores
    return re.sub(r'[\\/*?:"<>|]', '_', filename)

def download_video(video_url, output_path):
    yt = YouTube(video_url)
    stream = yt.streams.filter(progressive=True, file_extension='mp4').first()
    thumbnail_url = yt.thumbnail_url

    if stream:
        print(f"Downloading: {yt.title}")
        stream.download(output_path)
        print("Download completed!")

        # Download thumbnail
        sanitized_title = sanitize_filename(yt.title)
        thumbnail_file = os.path.join(output_path, f"{sanitized_title}_thumbnail.jpg")
        thumbnail_request = requests.get(thumbnail_url)
        with open(thumbnail_file, 'wb') as f:
            f.write(thumbnail_request.content)
        print("Thumbnail downloaded:", thumbnail_file)
    else:
        print(f"No downloadable streams found for video: {yt.title}")

def get_most_popular_video(api_key, channel_id):
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)

    request = youtube.search().list(
        part="snippet",
        channelId=channel_id,
        maxResults=1,
        order="viewCount"
    )
    response = request.execute()

    if 'items' in response and len(response['items']) > 0:
        video_id = response['items'][0]['id']['videoId']
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        return video_url
    else:
        print(f"No videos found for channel: {channel_id}")
        return None

def main():
    api_key = os.environ.get('YOUTUBE_API_KEY_1')
    if api_key is None:
        print("Please set your YouTube API key in the YOUTUBE_API_KEY environment variable.")
        return

    channels = [
        "UC_x5XG1OV2P6uZZ5FSM9Ttw",  # Example channel ID
        # Add more channel IDs to this list as needed
    ]
    num_videos = 1  # Download the most popular video of each channel

    for channel_id in channels:
        print(f"Fetching most popular video from channel: {channel_id}")
        popular_video_url = get_most_popular_video(api_key, channel_id)
        if popular_video_url:
            print(f"Downloading most popular video from channel: {channel_id}")
            download_video(popular_video_url, ".")  # Download to the current directory

if __name__ == "__main__":
    main()
