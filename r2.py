from googleapiclient.discovery import build
from bs4 import BeautifulSoup
import requests
import numpy as np
import matplotlib.pyplot as plt

# Function to scrape YouTube homepage
def scrape_youtube_homepage():
    url = 'https://www.youtube.com/'
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        print("Failed to fetch YouTube homepage.")
        return None

# Function to extract channels with most views and their video titles
def extract_channels_and_titles(html_content):
    # Implement web scraping logic here
    # Use BeautifulSoup to parse the HTML content and extract desired information
    pass

# Function to retrieve videos for a channel using YouTube API
def get_channel_videos(api_key, channel_id, max_results=50):
    youtube = build('youtube', 'v3', developerKey=api_key)
    request = youtube.search().list(
        part='snippet',
        channelId=channel_id,
        type='video',
        maxResults=max_results
    )
    response = request.execute()
    video_ids = [item['id']['videoId'] for item in response['items']]
    return video_ids

# Function to retrieve video view counts using YouTube API
def get_video_view_counts(api_key, video_ids):
    youtube = build('youtube', 'v3', developerKey=api_key)
    view_counts = []
    for video_id in video_ids:
        request = youtube.videos().list(
            part='statistics',
            id=video_id
        )
        response = request.execute()
        view_count = int(response['items'][0]['statistics']['viewCount'])
        view_counts.append(view_count)
    return view_counts

# Function to perform frequency distribution analysis and plot histogram
def perform_frequency_distribution_analysis(view_counts):
    max_view_count = max(view_counts)
    bins = np.arange(0, max_view_count + 1000, 1000)
    histogram, bins = np.histogram(view_counts, bins=bins)
    plt.bar(bins[:-1], histogram, width=np.diff(bins), edgecolor='black')
    plt.title('Frequency Distribution of Video View Counts')
    plt.xlabel('View Count')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.show()
    return histogram, bins

# Function to determine the best outcome channel
def determine_best_channel(channels_data):
    best_channel = None
    highest_peak = 0
    for channel_name, histogram_data in channels_data.items():
        peak = max(histogram_data[0])
        if peak > highest_peak:
            highest_peak = peak
            best_channel = channel_name
    return best_channel

# Main function
def main():
    # 1. Scrap from YouTube homepage
    html_content = scrape_youtube_homepage()

    # 2. Extract channels with most views and their video titles
    channels_and_titles = extract_channels_and_titles(html_content)

    # 3. Initialize dictionary to store channels' view counts
    channels_data = {}

    # 4. Retrieve view counts and perform frequency distribution analysis for each channel
    for channel_name, channel_info in channels_and_titles.items():
        # Retrieve videos for the channel using YouTube API
        video_ids = get_channel_videos(channel_info['api_key'], channel_info['channel_id'])

        # Retrieve video view counts using YouTube API
        view_counts = get_video_view_counts(channel_info['api_key'], video_ids)

        # Perform frequency distribution analysis
        histogram, bins = perform_frequency_distribution_analysis(view_counts)

        # Store histogram data for the channel
        channels_data[channel_name] = (histogram, bins)

    # 5. Determine the channel with the best outcome
    best_channel = determine_best_channel(channels_data)
    print(f"The channel with the best outcome is: {best_channel}")

if __name__ == "__main__":
    main()
