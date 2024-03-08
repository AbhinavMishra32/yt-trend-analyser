import os
import googleapiclient.discovery
from pytube import YouTube
import requests
import json
from colorama import Fore, Style

def progress_function(chunk, file_handle, bytes_remaining):
    global filesize
    current = ((filesize - bytes_remaining) / filesize)
    percent = ('{0:.1f}').format(current * 100)
    progress = int(50 * current)
    status = '█' * progress + '-' * (50 - progress)
    print(f'{Fore.CYAN} ↳ |{status}| {percent}%{Style.RESET_ALL}\r', end='', flush=True)

def download_video(video_url, output_path, channel_title):
    yt = YouTube(video_url, on_progress_callback=progress_function)
    
    try:
        global filesize
        filesize = yt.streams.filter(progressive=True, file_extension='mp4').first().filesize
    except AttributeError:
        print(f"{Fore.RED}The video '{yt.title}' is currently streaming live and cannot be downloaded.{Style.RESET_ALL}")
        return None, None

    stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
    if stream:
        video_title = yt.title.replace('/', '-')  # Remove invalid characters from the video title
        video_dir = os.path.join(output_path, channel_title, video_title)
        os.makedirs(video_dir, exist_ok=True)  # Create directory for the video
        print(f"{Fore.GREEN}\nDownloading: {yt.title} [{stream.resolution}]{Style.RESET_ALL}")
        try:
            video_path = os.path.join(video_dir, f"{video_title}.mp4")
            stream.download(video_dir)
            print(f"{Fore.GREEN}Download completed!{Style.RESET_ALL}")
            views = yt.views
            print(f"{Fore.YELLOW}Views: {views}{Style.RESET_ALL}")

            # Save thumbnail
            thumbnail_path = os.path.join(video_dir, f"{video_title}_thumbnail.jpg")
            thumbnail_url = yt.thumbnail_url
            thumbnail_data = requests.get(thumbnail_url).content
            with open(thumbnail_path, 'wb') as thumbnail_file:
                thumbnail_file.write(thumbnail_data)
            print(f"{Fore.GREEN}Thumbnail saved at: {thumbnail_path}{Style.RESET_ALL}")

            # Save video info as JSON
            info_json_path = os.path.join(video_dir, f"{video_title}_info.json")
            video_info = {
                "title": yt.title,
                "views": views,
                "description": yt.description,
                "thumbnail_url": thumbnail_url,
                "tags": yt.keywords,
                "length": yt.length,
                "rating": yt.rating,
                "author": yt.author,
                "publish_date": yt.publish_date.strftime("%Y-%m-%d"),
            }
            with open(info_json_path, "w") as info_json_file:
                json.dump(video_info, info_json_file, indent=4)
            print(f"{Fore.GREEN}Video info saved at: {info_json_path}{Style.RESET_ALL}")

            return video_path, views
        except Exception as e:
            print(f"{Fore.RED}An error occurred during download: {e}{Style.RESET_ALL}")
            return None, None
    else:
        print(f"{Fore.RED}No downloadable streams found for video: {yt.title}{Style.RESET_ALL}")
        return None, None

def get_most_popular_videos(api_key, channel_id, num_videos):
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)

    request = youtube.search().list(
        part="snippet",
        channelId=channel_id,
        maxResults=num_videos * 2,  # Fetch more videos to ensure we have enough non-live ones
        order="viewCount"
    )
    response = request.execute()

    popular_videos = []
    for item in response.get('items', []):
        video_id = item['id']['videoId']
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        # Check if the video is live
        if 'liveBroadcastContent' in item['snippet'] and item['snippet']['liveBroadcastContent'] == 'live':
            continue  # Skip live videos
        popular_videos.append((video_url, item['snippet']['channelTitle']))
        if len(popular_videos) == num_videos:
            break

    if len(popular_videos) < num_videos:
        print(f"{Fore.RED}Not enough non-live videos found for channel: {channel_id}{Style.RESET_ALL}")

    return popular_videos

def main():
    api_key = os.environ.get('YOUTUBE_API_KEY_1')
    if api_key is None:
        print(f"{Fore.RED}Please set your YouTube API key in the YOUTUBE_API_KEY environment variable.{Style.RESET_ALL}")
        return

    channels = [
        "UC-CSyyi47VX1lD9zyeABW3w",  # Example channel ID
        # Add more channel IDs to this list as needed
    ]

    num_videos_to_download = 3  # Choose the number of videos to download

    output_folder = "downloaded_videos"  # Define the output folder for downloaded videos

    for channel_id in channels:
        print(f"{Fore.YELLOW}Fetching most popular videos from channel: {channel_id}{Style.RESET_ALL}")
        popular_videos = get_most_popular_videos(api_key, channel_id, num_videos_to_download)
        for video_url, channel_title in popular_videos:
            print(f"{Fore.YELLOW}Downloading popular video from channel: {channel_id}{Style.RESET_ALL}")
            video_path, views = download_video(video_url, output_folder, channel_title)  
            if video_path:
                print(f"{Fore.GREEN}Video downloaded and saved in folder: {os.path.dirname(video_path)}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
