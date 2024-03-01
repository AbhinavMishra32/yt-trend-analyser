import os
import moviepy.editor as mp
import math
from PIL import Image
import numpy
import subprocess
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_audioclips, CompositeAudioClip

def extract_frames(output_folder):
    """
    Retrieves existing image files from a folder.

    Parameters:
        output_folder (str): Path to the folder containing image files.

    Returns:
        List: A list of image file paths.
    """
    # List all image files in the output folder
    images = [f for f in os.listdir(output_folder) if not f.startswith('.') and f.endswith('.jpg')]

    # Return the list of image file paths
    return [os.path.join(output_folder, image) for image in images]


def zoom_in_effect(clip, zoom_ratio=0.04):
    def effect(get_frame, t):
        img = Image.fromarray(get_frame(t))
        base_size = img.size

        new_size = (
            math.ceil(img.size[0] * (1 + (zoom_ratio * t))),
            math.ceil(img.size[1] * (1 + (zoom_ratio * t)))
        )

        # The new dimensions must be even.
        new_size = (
            new_size[0] + (new_size[0] % 2),
            new_size[1] + (new_size[1] % 2)
        )

        img = img.resize(new_size, Image.LANCZOS)

        x = math.ceil((new_size[0] - base_size[0]) / 2)
        y = math.ceil((new_size[1] - base_size[1]) / 2)

        img = img.crop((
            x, y, new_size[0] - x, new_size[1] - y
        )).resize(base_size, Image.LANCZOS)

        result = numpy.array(img)
        img.close()

        return result

    return clip.fl(effect)


def create_slideshow(image_files, image_duration, total_duration):
    """Create a slideshow from image files."""
    clips = []
    total_duration_remaining = total_duration
    for image_path in image_files:
        # If this is the last image, adjust its duration so that the total duration matches the desired length
        if total_duration_remaining < image_duration:
            image_duration = total_duration_remaining

        # Load image file as a MoviePy clip
        clip = mp.ImageClip(image_path).set_duration(image_duration)  

        # Apply the zoom effect
        slide = zoom_in_effect(clip, zoom_ratio=0.04) 

        clips.append(slide)
        total_duration_remaining -= image_duration
        if total_duration_remaining <= 0:
            break
    
    return mp.concatenate_videoclips(clips)


def get_mp3_duration(file_path):
    audio = mp.AudioFileClip(file_path)
    duration_sec = audio.duration
    audio.close()
    return duration_sec


# Parameters
images_folder = "output_frames"  # Folder containing extracted frames
total_duration = get_mp3_duration("script_audio.mp3") # Total duration of the video in seconds
output_file = "slideshow.mp4"  # Output file name
resolution = (1280, 720)  # Default resolution

# Create slideshow from extracted frames
frame_files = extract_frames(images_folder)

# Calculate image_duration based on total_duration and number of images
image_duration = total_duration / len(frame_files)

# Create the slideshow video
slideshow = create_slideshow(frame_files, image_duration, total_duration)

# Set video resolution
slideshow = slideshow.resize(resolution) #type: ignore

# Export slideshow to a file with specified codec, threads, and resolution
slideshow.write_videofile(output_file, fps=24, codec='libx264', threads=4, verbose=False, audio_codec ="aac")

# Use ffmpeg to concatenate slideshow video with audio file
ffmpeg_command = [
    "ffmpeg",
    "-i", output_file,
    "-i", "script_audio.mp3",
    "-c:v", "copy",
    "-c:a", "aac",
    "-strict", "experimental",
    "-shortest",
    "intermediate_video.mp4"
]
subprocess.run(ffmpeg_command)

# Load video
video = VideoFileClip("intermediate_video.mp4")

# Load main audio (voice of the person)
main_audio = AudioFileClip("script_audio.mp3")

# Set the background music folder
background_music_folder = "background_music"

# Get all the MP3 files in the background music folder
background_music_files = [os.path.join(background_music_folder, f) for f in os.listdir(background_music_folder) if f.endswith('.mp3')]

# Load background music files, adjust the volume, and concatenate
background_music_clips = [AudioFileClip(music).volumex(0.05) for music in background_music_files]  # Adjust the volume as needed
background_music = concatenate_audioclips(background_music_clips)

# Make the background music match the duration of the main audio
background_music = background_music.subclip(0, main_audio.duration)

# Combine main audio and background music
combined_audio = CompositeAudioClip([main_audio, background_music])

# Set the audio of the video
video = video.set_audio(combined_audio)

# Write the result to a file
video.write_videofile("final_video.mp4", fps=24, codec='libx264', threads=4, verbose=False, audio_codec ="aac")
