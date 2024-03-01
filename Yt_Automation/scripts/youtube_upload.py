import sys
import requests
from selenium_youtube import Youtube
from selenium_chrome import Chrome

chrome = Chrome()
youtube = Youtube(browser=chrome)  # or firefox

def get_movie_cast(movie_title):
    # Replace 'YOUR_API_KEY' with your actual API key
    api_key = 'YOUR_API_KEY'
    url = f'http://www.omdbapi.com/?apikey={api_key}&t={movie_title}'
    response = requests.get(url)
    data = response.json()
    
    if response.status_code == 200 and data['Response'] == 'True':
        cast_list = data['Actors'].split(', ')
        return cast_list
    else:
        print("Error: Movie not found or API request failed.")
        return None

def generate_video_title(movie_title, max_cast_members=3):
    cast = get_movie_cast(movie_title)
    if cast:
        # Slice the cast list to include only the first few members
        cast_str = ' | '.join(cast[:max_cast_members])
        title = f"{movie_title} Full Movie | {cast_str} | Full Facts"
        return title
    else:
        return None

def main():
    # Check if movie title is provided as command-line argument
    if len(sys.argv) < 2:
        print("Please provide the movie title as a command-line argument.")
        return


    movie_title = ' '.join(sys.argv[1:])  # Concatenate all arguments after the script name
    title = generate_video_title(movie_title)
    if title:
        print("Generated video title:", title)
        # Upload the video with the generated title and description
        description = open('description.txt', 'r').read()
        tags = open('tags.txt', 'r').read().split(',')
        upload_result = youtube.upload('final_video.mp4', title, description, tags)
        print("Upload result:", upload_result)
    else:
        print("Could not generate video title.")

if __name__ == "__main__":
    main()
