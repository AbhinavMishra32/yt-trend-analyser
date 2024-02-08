import re
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def scrape_youtube_channel_ids():
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
                        channel_ids.append(channel_id)

    return channel_ids

if __name__ == "__main__":
    channel_ids = scrape_youtube_channel_ids()
    print("Channel IDs:")
    for channel_id in channel_ids:
        print(channel_id)
