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
        print("Successfully fetched YouTube homepage.")
        print(response.content)  # Uncomment to print HTML content
        with open('youtube_homepage.html', 'wb') as file:
            file.write(response.content)
        return response.content
    else:
        print("Failed to fetch YouTube homepage.")
        return None

# Function to extract channels with most views and their video titles
def extract_channels_and_titles(html_content):
    channels_and_titles = {}
    if html_content:
        soup = BeautifulSoup(html_content, 'html.parser')
        # Find all channel containers
        channel_containers = soup.find_all('div', class_='ytd-rich-grid-video-renderer')
        for channel_container in channel_containers:
            # Extract channel name
            channel_name_element = channel_container.find('a', class_='yt-simple-endpoint style-scope ytd-rich-grid-video-renderer')
            if channel_name_element:
                channel_name = channel_name_element.text.strip()
                # Extract video titles
                video_titles = [title.text.strip() for title in channel_container.find_all('a', id='video-title')]
                channels_and_titles[channel_name] = {'video_titles': video_titles}
                print(f"Channel: {channel_name}")
                print(f"Video Titles: {video_titles}")
    return channels_and_titles



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
def perform_frequency_distribution_analysis(view_counts, channel_name):
    max_view_count = max(view_counts)
    bins = np.arange(0, max_view_count + 1000, 1000)
    histogram, bins = np.histogram(view_counts, bins=bins)
    plt.bar(bins[:-1], histogram, width=np.diff(bins), edgecolor='black')
    plt.title(f'Frequency Distribution of Video View Counts for {channel_name}')
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
    # Your YouTube API key
    api_key = 'AIzaSyAenhBhQR18CWckisOHKxcDi75JJEwHf4I'

    # 1. Scrap from YouTube homepage
    html_content = scrape_youtube_homepage()

    # 2. Extract channels with most views and their video titles
    channels_and_titles = extract_channels_and_titles(html_content)

    if channels_and_titles:
        # 3. Initialize dictionary to store channels' view counts
        channels_data = {}

        # 4. Retrieve view counts and perform frequency distribution analysis for each channel
        for channel_name, channel_info in channels_and_titles.items():
            print(f"Processing channel: {channel_name}")
            # Retrieve videos for the channel using YouTube API
            video_ids = get_channel_videos(api_key, channel_info['channel_id'])
            print(f"Found {len(video_ids)} videos for channel: {channel_name}")

            # Retrieve video view counts using YouTube API
            view_counts = get_video_view_counts(api_key, video_ids)
            print(f"Retrieved view counts for videos of channel: {channel_name}")

            # Perform frequency distribution analysis
            histogram, bins = perform_frequency_distribution_analysis(view_counts, channel_name)

            # Store histogram data for the channel
            channels_data[channel_name] = (histogram, bins)

        # 5. Determine the channel with the best outcome
        best_channel = determine_best_channel(channels_data)
        print(f"The channel with the best outcome is: {best_channel}")
    else:
        print("No channels and titles extracted from the YouTube homepage.")

if __name__ == "__main__":
    main()
