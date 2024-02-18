import os
import googleapiclient.discovery
import requests
from pytube import YouTube

def sanitize_filename(filename):
    return "".join([c for c in filename if c.isalpha() or c.isdigit() or c==' ']).rstrip()

def download_video(video_url, output_path, preferred_resolution=None):
    yt = YouTube(video_url)
    
    # Filter streams with both video and audio
    streams = yt.streams.filter(progressive=True, file_extension='mp4')
    
    if preferred_resolution:
        # Filter streams by preferred resolution
        streams = [stream for stream in streams if stream.resolution == preferred_resolution]

    if streams:
        stream = streams[0]  # Choose the first stream
        print(f"Downloading: {yt.title} ({stream.resolution})")
        stream.download(output_path)
        print("Download completed!")

        # Download thumbnail
        sanitized_title = sanitize_filename(yt.title)
        thumbnail_file = os.path.join(output_path, f"{sanitized_title}_thumbnail.jpg")
        thumbnail_request = requests.get(yt.thumbnail_url)
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
    preferred_resolution = "720p"  # Change this to your preferred resolution

    for channel_id in channels:
        print(f"Fetching most popular video from channel: {channel_id}")
        popular_video_url = get_most_popular_video(api_key, channel_id)
        if popular_video_url:
            print(f"Downloading most popular video from channel: {channel_id}")
            download_video(popular_video_url, ".", preferred_resolution=preferred_resolution)  # Download to the current directory

if __name__ == "__main__":
    main()
