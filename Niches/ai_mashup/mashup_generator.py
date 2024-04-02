import os
import random
import datetime
from pydub import AudioSegment

MAX_DURATION = 1200  # 20 minutes in seconds

# Get the list of new songs
new_songs_dir = os.path.join(os.getcwd(), 'new_songs')
new_songs = [os.path.join(new_songs_dir, f) for f in os.listdir(new_songs_dir) if f.endswith(('.wav', '.mp3'))]

# Get the list of old songs
old_songs_dir = os.path.join(os.getcwd(), 'old_songs')
old_songs = [os.path.join(old_songs_dir, f) for f in os.listdir(old_songs_dir) if f.endswith(('.wav', '.mp3'))]

# Create a new mashup
new_mashup = AudioSegment.empty()

# Add new songs
new_songs_used = [os.path.splitext(os.path.basename(song))[0] for song in new_songs]
for song in new_songs:
    new_mashup += AudioSegment.from_file(song)

# Add random old songs until duration limit is reached
random.shuffle(old_songs)
old_songs_used = []
for song in old_songs:
    audio = AudioSegment.from_file(song)
    if len(new_mashup) + len(audio) > MAX_DURATION * 1000:  # Convert to milliseconds
        break
    new_mashup += audio
    old_songs_used.append(os.path.splitext(os.path.basename(song))[0])

# Export the mashup
mashup_file = os.path.join(os.getcwd(), 'mashup.wav')
new_mashup.export(mashup_file, format='wav')

# Move new songs to old songs folder and rename
max_index = max([int(f.split('.')[0]) for f in os.listdir(old_songs_dir) if f.endswith(('.wav', '.mp3'))], default=0)
for i, song in enumerate(new_songs, start=max_index+1):
    src = song
    dst = os.path.join(old_songs_dir, f"{i}.{song.split('.')[-1]}")
    os.rename(src, dst)

# Write the mashup information to a text file
mashup_info_file = os.path.join(os.getcwd(), 'mashup_info.txt')
try:
    with open(mashup_info_file, 'r') as f:
        existing_mashups = f.readlines()
except FileNotFoundError:
    existing_mashups = []

mashup_no = len(existing_mashups) + 1

current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
songs_used = ','.join(new_songs_used + old_songs_used)
with open(mashup_info_file, 'a') as f:
    f.write(f"Date: {current_time}, Mashup No: {mashup_no}, Songs Used: {songs_used}\n")