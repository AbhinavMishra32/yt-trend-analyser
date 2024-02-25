from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_audioclips

# Load video
video = VideoFileClip("video.mp4")

# Load main audio (voice of the person)
main_audio = AudioFileClip("main_audio.mp3")

# Load background music files
background_music_files = ["music1.mp3", "music2.mp3", "music3.mp3"]
background_music_clips = [AudioFileClip(music) for music in background_music_files]

# Concatenate background music clips
background_music = concatenate_audioclips(background_music_clips)

# Lower the volume of the background music
background_music = background_music.volumex(0.1)

# Combine main audio and background music
combined_audio = main_audio.overlay(background_music)

# Set the audio of the video
video = video.set_audio(combined_audio)

# Write the result to a file
video.write_videofile("output.mp4")