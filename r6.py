import os
import re
import json
import matplotlib.pyplot as plt
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from googleapiclient.discovery import build

# YouTube API key
API_KEY = "AIzaSyAenhBhQR18CWckisOHKxcDi75JJEwHf4I"

def scrape_youtube_channel_names():
    # Setting up Selenium WebDriver with Chrome
    options = Options()
    options.add_argument("--incognito")  # Open in incognito mode
    driver = webdriver.Chrome(options=options)
    
    # Open YouTube homepage
    driver.get("https://www.youtube.com")
    
    # Getting page source
    page_source = driver.page_source
    
    # Close the WebDriver
    driver.quit()
    
    # Extract channel names from JSON data
    channel_names = []

    # Use regular expressions to find JSON data
    pattern = re.compile(r'ytInitialData\s*=\s*({.*?});', re.DOTALL)
    match = pattern.search(page_source)
    if match:
        json_data = match.group(1)

        # Parsing JSON data
        data = json.loads(json_data)
        contents = data.get("contents", {}).get("twoColumnBrowseResultsRenderer", {}).get("tabs", [])
        for tab in contents:
            rich_grid_renderer = tab.get("tabRenderer", {}).get("content", {}).get("richGridRenderer", {})
            for content in rich_grid_renderer.get("contents", []):
                rich_item_renderer = content.get("richItemRenderer", {})
                video_renderer = rich_item_renderer.get("content", {}).get("videoRenderer", {})
                if video_renderer:
                    long_byline_text = video_renderer.get("longBylineText", {}).get("runs", [])[0]
                    channel_names.append(long_byline_text.get("text", ""))

    return channel_names

def get_channel_videos(channel_id, max_results=50):
    youtube = build("youtube", "v3", developerKey=API_KEY)

    # Fetch videos from the channel
    request = youtube.search().list(
        part="snippet",
        channelId=channel_id,
        maxResults=max_results,
        order="date",
        type="video"
    )
    response = request.execute()
    
    videos = []
    for item in response['items']:
        video = {
            'title': item['snippet']['title'],
            'viewCount': get_video_stats(item['id']['videoId'])  # Fetch view count
        }
        videos.append(video)
    
    return videos

def get_video_stats(video_id):
    youtube = build("youtube", "v3", developerKey=API_KEY)

    # Fetch video statistics
    request = youtube.videos().list(
        part="statistics",
        id=video_id
    )
    response = request.execute()

    return int(response['items'][0]['statistics']['viewCount'])

def plot_histogram(data, title):
    plt.hist(data, bins=20, color='blue', alpha=0.7)
    plt.title(title)
    plt.xlabel('View Count')
    plt.ylabel('Frequency')
    plt.show()

if __name__ == "__main__":
    # Scraping channel names from YouTube homepage
    channel_names = scrape_youtube_channel_names()

    # Choose a subset of channels from the list
    num_channels = 5
    selected_channels = channel_names[:num_channels]

    # Fetch videos from selected channels
    videos_data = {}
    for channel_name in selected_channels:
        # Assuming channel name matches the channel ID
        videos_data[channel_name] = get_channel_videos(channel_name)

    # Extract view counts for frequency distribution analysis
    view_counts = []
    for videos in videos_data.values():
        for video in videos:
            view_counts.append(video['viewCount'])

    # Plot histogram
    plot_histogram(view_counts, 'View Count Distribution')
