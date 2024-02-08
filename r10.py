import os
import re
import json
import logging
import random
import datetime
import seaborn as sns
import matplotlib.pyplot as plt
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from googleapiclient.discovery import build
from colorlog import ColoredFormatter

# Global constants
NUM_VIDEOS_PER_CHANNEL = 1
USE_SAMPLE_DATA = False  # Set to True to use sample data, False to use YouTube API
NUM_CHANNELS_TO_FETCH = 2  # Limit for the number of channels to fetch

# YouTube API key
key1 = "AIzaSyAfhdh3raVJa6DYYl6J1An5hSPG2Cgk_uc"
key2 = "AIzaSyDzmYzLX4bEv-ADzy23oBgqWbjZ2skb8Bo"
API_KEY = key2

# Fetch order options
FETCH_ORDER_FIRST_TO_LAST = "first_to_last"
FETCH_ORDER_LAST_TO_FIRST = "last_to_first"

# Fetch order
FETCH_ORDER = FETCH_ORDER_FIRST_TO_LAST  # Change this to choose the fetch order

# Output file name
OUTPUT_JSON_FILE = "video_data.json"

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

def calculate_channel_age(channel_id):
    try:
        youtube = build("youtube", "v3", developerKey=API_KEY)

        # Fetch channel details
        request = youtube.channels().list(
            part="snippet",
            id=channel_id
        )
        response = request.execute()

        # Extract channel creation date
        creation_date_str = response['items'][0]['snippet']['publishedAt']
        logger.info("Creation date string: %s", creation_date_str)

        try:
            # Attempt to parse the datetime string with microseconds
            creation_date = datetime.datetime.strptime(creation_date_str, "%Y-%m-%dT%H:%M:%S.%fZ").date()
        except ValueError:
            # If parsing with microseconds fails, try parsing without microseconds
            creation_date = datetime.datetime.strptime(creation_date_str[:-5], "%Y-%m-%dT%H:%M:%S").date()

        # Calculate channel age
        current_date = datetime.date.today()
        channel_age_days = (current_date - creation_date).days

        return channel_age_days
    except Exception as e:
        logger.error("Error occurred while calculating channel age for channel ID %s: %s", channel_id, str(e))
        return -1  # Return -1 if unable to calculate channel age












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
                            channel_name = video_renderer.get("longBylineText", {}).get("runs", [])[0].get("text", "")
                            channel_age = calculate_channel_age(channel_id)  # Calculate channel age
                            channel_ids.append((channel_id, channel_name, channel_age))

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
            published_at = item['snippet']['publishedAt'][:-1]  # Remove the last character (microseconds indicator)
            logger.info(f"Fetching video {index + 1} for channel {channel_id}: {video_title} (ID: {video_id})")
            video = {
                'title': video_title,
                'viewCount': get_video_stats(video_id),  # Fetch view count
                'channel': channel_id,
                'channel_name': item['snippet']['channelTitle'],
                'publishedAt': published_at  # Include published timestamp in video data
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


def calculate_upload_frequency(videos):
    upload_dates = [video['publishedAt'] for video in videos]
    upload_dates.sort(reverse=True)  # Sort in descending order to calculate frequency
    upload_intervals = []
    
    possible_formats = ["%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%M:%S"]
    
    for i in range(len(upload_dates) - 1):
        date1 = None
        date2 = None
        for format in possible_formats:
            try:
                date1 = datetime.datetime.strptime(upload_dates[i], format)
                date2 = datetime.datetime.strptime(upload_dates[i + 1], format)
                break  # If parsing succeeds, break out of the loop
            except ValueError:
                pass  # If parsing fails, try the next format
        
        if date1 is not None and date2 is not None:
            interval = (date1 - date2).days  # Calculate the difference in days between consecutive uploads
            upload_intervals.append(interval)
        else:
            print(f"Skipping invalid datetime string: {upload_dates[i]}")

    median_frequency = None
    mean_frequency = None
    if upload_intervals:
        median_frequency = upload_intervals[len(upload_intervals) // 2] if len(upload_intervals) % 2 != 0 else (upload_intervals[len(upload_intervals) // 2] + upload_intervals[len(upload_intervals) // 2 - 1]) / 2
        mean_frequency = sum(upload_intervals) / len(upload_intervals)

    return median_frequency, mean_frequency




def generate_sample_data(channel_id):
    # Generate sample data randomly
    sample_videos = []
    for i in range(NUM_VIDEOS_PER_CHANNEL):
        video = {
            'title': f'Sample Video {i+1} for Channel {channel_id}',
            'viewCount': random.randint(1000, 1000000),
            'channel': channel_id,
            'channel_name': f'Channel {channel_id}',
            'publishedAt': datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")  # Current timestamp as placeholder
        }
        sample_videos.append(video)
    return sample_videos


def save_data_to_json(data, filename):
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)


if __name__ == "__main__":
    # Set Seaborn style
    sns.set(style="whitegrid")

    # Scraping channel IDs from YouTube homepage
    channel_ids = scrape_youtube_channel_ids()

    if channel_ids:
        # Fetch videos from selected channels
        videos_data = {}
        for channel_id, channel_name, channel_age in channel_ids:
            if USE_SAMPLE_DATA:
                videos_data[channel_id] = generate_sample_data(channel_id)
            else:
                videos_data[channel_id] = get_channel_videos(channel_id)

            # Calculate upload frequency
            median_frequency, mean_frequency = calculate_upload_frequency(videos_data[channel_id])

            # Add channel age and upload frequency to each video
            for video in videos_data[channel_id]:
                video['channel_age'] = channel_age
                video['median_upload_frequency'] = median_frequency
                video['mean_upload_frequency'] = mean_frequency

        # Save videos data to JSON file
        save_data_to_json(videos_data, OUTPUT_JSON_FILE)

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
        logger.warning("No channel IDs found. Exiting without saving data to JSON.")
