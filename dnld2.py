import os
import googleapiclient.discovery
from pytube import YouTube
import requests

def progress_function(chunk, file_handle, bytes_remaining):
    global filesize
    current = ((filesize - bytes_remaining) / filesize)
    percent = ('{0:.1f}').format(current * 100)
    progress = int(50 * current)
    status = '█' * progress + '-' * (50 - progress)
    print(f' ↳ |{status}| {percent}%\r', end='', flush=True)

def download_video(video_url, output_path, channel_title):
    yt = YouTube(video_url, on_progress_callback=progress_function)
    global filesize
    filesize = yt.streams.filter(progressive=True, file_extension='mp4').first().filesize
    stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
    if stream:
        video_title = yt.title.replace('/', '-')  # Remove invalid characters from the video title
        video_dir = os.path.join(output_path, channel_title, video_title)
        os.makedirs(video_dir, exist_ok=True)  # Create directory for the video
        print(f"\nDownloading: {yt.title} [{stream.resolution}]")
        try:
            video_path = os.path.join(video_dir, f"{video_title}.mp4")
            stream.download(video_dir)
            print("Download completed!")
            return video_path
        except Exception as e:
            print(f"An error occurred during download: {e}")
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
        return video_url, response['items'][0]['snippet']['channelTitle']
    else:
        print(f"No videos found for channel: {channel_id}")
        return None, None

def main():
    api_key = os.environ.get('YOUTUBE_API_KEY_1')
    if api_key is None:
        print("Please set your YouTube API key in the YOUTUBE_API_KEY environment variable.")
        return

    channels = [
        "UChWdyc0gPwjdyC2LiZxRbyQ",  # Example channel ID
        # Add more channel IDs to this list as needed
    ]

    output_folder = "downloaded_videos"  # Define the output folder for downloaded videos

    for channel_id in channels:
        print(f"Fetching most popular video from channel: {channel_id}")
        popular_video_url, channel_title = get_most_popular_video(api_key, channel_id)
        if popular_video_url:
            print(f"Downloading most popular video from channel: {channel_id}")
            video_path = download_video(popular_video_url, output_folder, channel_title)  
            if video_path:
                thumbnail_path = os.path.join(output_folder, channel_title, f"{channel_title}_thumbnail.jpg")
                thumbnail_url = YouTube(popular_video_url).thumbnail_url
                try:
                    thumbnail_data = requests.get(thumbnail_url).content
                    with open(thumbnail_path, 'wb') as thumbnail_file:
                        thumbnail_file.write(thumbnail_data)
                    print(f"Thumbnail saved at: {thumbnail_path}")
                except Exception as e:
                    print(f"An error occurred while saving the thumbnail: {e}")

if __name__ == "__main__":
    main()
