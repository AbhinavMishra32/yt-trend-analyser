import sys
import requests


def get_movie_cast(movie_title):
    # Replace 'YOUR_API_KEY' with your actual API key
    api_key = 'c7567a52'
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
    
movie_title = ' '.join(sys.argv[1:])  # Concatenate all arguments after the script name

title = generate_video_title(movie_title)

with open('title.txt', 'w') as f:
    f.write(title or "No title available")

description = open('description.txt', 'r').read()
tags = open('tags.txt', 'r').read().split(',')