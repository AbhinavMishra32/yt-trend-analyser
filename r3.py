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
    with open("youtube_homepage2.html", "w") as f:
        f.write(page_source)
    return page_source

if __name__ == "__main__":
    page_source = scrape_youtube_channel_names()
    print(page_source)
