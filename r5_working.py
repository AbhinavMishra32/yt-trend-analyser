import re
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

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
    
    # Extract channel names and video titles from JSON data
    channel_names = []
    video_titles = []

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
                    video_title = video_renderer.get("title", {}).get("runs", [])[0]
                    video_titles.append(video_title.get("text", ""))

    return channel_names, video_titles

if __name__ == "__main__":
    channel_names, video_titles = scrape_youtube_channel_names()
    print("Channel Names:")
    for name in channel_names:
        print(name)
    print("\nVideo Titles:")
    for title in video_titles:
        print(title)
