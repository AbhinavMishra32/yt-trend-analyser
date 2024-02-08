from selenium import webdriver

def get_html(url):
    driver = webdriver.Chrome()  # or webdriver.Chrome(), depending on your preference
    driver.get(url)
    html = driver.page_source
    driver.quit()
    return html

url = 'https://youtube.com/'  # replace with your url
html = get_html(url)
print(html)