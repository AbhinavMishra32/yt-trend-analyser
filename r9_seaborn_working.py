import os
import re
import json
import logging
import random
import seaborn as sns
import matplotlib.pyplot as plt
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from googleapiclient.discovery import build
from colorlog import ColoredFormatter

# Global constants
NUM_VIDEOS_PER_CHANNEL = 5
USE_SAMPLE_DATA = False  # Set to True to use sample data, False to use YouTube API
NUM_CHANNELS_TO_FETCH = 5  # Limit for the number of channels to fetch

# YouTube API key
API_KEY = "AIzaSyAfhdh3raVJa6DYYl6J1An5hSPG2Cgk_uc"

# Fetch order options
FETCH_ORDER_FIRST_TO_LAST = "first_to_last"
FETCH_ORDER_LAST_TO_FIRST = "last_to_first"

# Fetch order
FETCH_ORDER = FETCH_ORDER_FIRST_TO_LAST  # Change this to choose the fetch order

# Configure logging
formatter = ColoredFormatter(
    "%(asctime)s - %(log_color)s%(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    log_colors={
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'red,bg_white',
    }
)
logger = logging.getLogger(__name__)
console = logging.StreamHandler()
console.setFormatter(formatter)
logger.addHandler(console)
logger.setLevel(logging.INFO)

def scrape_youtube_channel_ids():
    logger.info("Scraping YouTube homepage to obtain channel IDs...")
    try:
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

        # Extract channel IDs from JSON data
        channel_ids = []

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
                        channel_id = video_renderer.get("longBylineText", {}).get("runs", [])[0].get("navigationEndpoint", {}).get("browseEndpoint", {}).get("browseId", "")
                        if channel_id:
                            channel_ids.append((channel_id, video_renderer.get("longBylineText", {}).get("runs", [])[0].get("text", "")))

        logger.info("Channel IDs obtained successfully.")
        return channel_ids[:NUM_CHANNELS_TO_FETCH]  # Limit the number of channels fetched
    except Exception as e:
        logger.error("Error occurred while scraping YouTube channel IDs: %s", str(e))
        return []

def get_channel_videos(channel_id, max_results=NUM_VIDEOS_PER_CHANNEL):
    try:
        youtube = build("youtube", "v3", developerKey=API_KEY)

        # Fetch videos from the channel
        if FETCH_ORDER == FETCH_ORDER_FIRST_TO_LAST:
            order = "date"
        elif FETCH_ORDER == FETCH_ORDER_LAST_TO_FIRST:
            order = "-date"
        else:
            logger.error("Invalid fetch order specified.")
            return []

        request = youtube.search().list(
            part="snippet",
            channelId=channel_id,
            maxResults=max_results,
            order=order,
            type="video"
        )
        response = request.execute()

        videos = []
        for index, item in enumerate(response['items']):
            video_title = item['snippet']['title']
            video_id = item['id']['videoId']
            logger.info(f"Fetching video {index + 1} for channel {channel_id}: {video_title} (ID: {video_id})")
            video = {
                'title': video_title,
                'viewCount': get_video_stats(video_id),  # Fetch view count
                'channel': channel_id,
                'channel_name': item['snippet']['channelTitle']
            }
            videos.append(video)

        if FETCH_ORDER == FETCH_ORDER_LAST_TO_FIRST:
            videos.reverse()  # Reverse the order if fetching from last to first

        return videos
    except Exception as e:
        logger.error("Error occurred while fetching videos for channel ID %s: %s", channel_id, str(e))
        return []

def get_video_stats(video_id):
    try:
        youtube = build("youtube", "v3", developerKey=API_KEY)

        # Fetch video statistics
        request = youtube.videos().list(
            part="statistics",
            id=video_id
        )
        response = request.execute()

        return int(response['items'][0]['statistics']['viewCount'])
    except Exception as e:
        logger.error("Error occurred while fetching statistics for video ID %s: %s", video_id, str(e))
        return 0

def generate_sample_data(channel_id):
    # Generate sample data randomly
    sample_videos = []
    for i in range(NUM_VIDEOS_PER_CHANNEL):
        video = {
            'title': f'Sample Video {i+1} for Channel {channel_id}',
            'viewCount': random.randint(1000, 1000000),
            'channel': channel_id,
            'channel_name': f'Channel {channel_id}'
        }
        sample_videos.append(video)
    return sample_videos

def plot_channel_histogram(channel_id, videos, title):
    view_counts = [video['viewCount'] for video in videos]
    plt.figure(figsize=(10, 6))
    sns.histplot(view_counts, bins=20, kde=True, color='blue')
    plt.title(title)
    plt.xlabel('View Count')
    plt.ylabel('Frequency')
    plt.show()

def plot_histograms(videos_data):
    for channel_id, videos in videos_data.items():
        title = f'View Count Distribution for Channel {videos[0]["channel_name"]} (ID: {channel_id})'
        plot_channel_histogram(channel_id, videos, title)

if __name__ == "__main__":
    # Set Seaborn style
    sns.set(style="whitegrid")

    # Scraping channel IDs from YouTube homepage
    channel_ids = scrape_youtube_channel_ids()

    if channel_ids:
        # Fetch videos from selected channels
        videos_data = {}
        for channel_id, channel_name in channel_ids:
            if USE_SAMPLE_DATA:
                videos_data[channel_id] = generate_sample_data(channel_id)
            else:
                videos_data[channel_id] = get_channel_videos(channel_id)

        # Plot histograms for each channel
        plot_histograms(videos_data)

        # Perform frequency distribution analysis
        for channel_id, videos in videos_data.items():
            view_counts = [video['viewCount'] for video in videos]
            max_views = max(view_counts)
            score = 0
            for views in view_counts:
                if views > max_views:
                    score += 1
                    max_views = views
            print(f'Frequency distribution score for Channel {videos[0]["channel_name"]} (ID: {channel_id}): {score}')
    else:
        logger.warning("No channel IDs found. Exiting without plotting histogram.")
