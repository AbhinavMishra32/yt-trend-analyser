import youtube_dl
import json
import re

import youtube_dl
import json
import re

def download_videos(channel_name, num_videos):
    ydl_opts = {
        'quiet': False,
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': '%(title)s.%(ext)s',
        'noplaylist': True,  # Avoid downloading the entire playlist
        'max_downloads': num_videos  # Limit the number of videos to download
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([f'https://www.youtube.com/c/{channel_name}/videos'])

def main():
    choice = input("Enter '1' to provide a specific channel name or '2' to provide a JSON array of channel names: ")

    if choice == '1':
        channel_name = input("Enter the name of the YouTube channel: ")
        num_videos = int(input("Enter the number of videos to download: "))
        download_videos(channel_name, num_videos)
    elif choice == '2':
        json_file = input("Enter the path to the JSON file containing channel names: ")
        num_videos = int(input("Enter the number of videos to download from each channel: "))
        try:
            with open(json_file, 'r') as f:
                channels = json.load(f)
                for channel in channels:
                    download_videos(channel, num_videos)
        except FileNotFoundError:
            print("File not found. Please provide a valid path to the JSON file.")
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()
