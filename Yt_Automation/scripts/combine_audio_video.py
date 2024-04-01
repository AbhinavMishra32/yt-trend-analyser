import os
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_audioclips, CompositeAudioClip

# Load video
video = VideoFileClip("slideshow.mp4")

# Load main audio (voice of the person)
main_audio = AudioFileClip("script_audio.mp3")

# Set the background music folder
background_music_folder = "background_music"

# Get all the MP3 files in the background music folder
background_music_files = [os.path.join(background_music_folder, f) for f in os.listdir(background_music_folder) if f.endswith('.mp3')]

# Load background music files, adjust the volume, and concatenate
background_music_clips = [AudioFileClip(music).volumex(0.03) for music in background_music_files]  # Adjust the volume as needed
background_music = concatenate_audioclips(background_music_clips)

# Make the background music match the duration of the main audio
background_music = background_music.subclip(0, main_audio.duration)

# Combine main audio and background music
combined_audio = CompositeAudioClip([main_audio, background_music])

# Print debug information
print("Main audio duration:", main_audio.duration)
print("Background music duration:", background_music.duration)
print("Combined audio duration:", combined_audio.duration)

# Set the audio of the video
video = video.set_audio(combined_audio)

# Print debug information
print("Video duration:", video.duration)

# Write the result to a file
video.write_videofile("sub_video.mp4", fps=24, codec='libx264', threads=4, verbose=False, audio_codec ="aac")
