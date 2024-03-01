"""
Put in scripts folder instead of old_scripts for the paths to work!
"""

import subprocess
import os
from mutagen.mp3 import MP3

def main():
    output_folder = "scripts/output_frames"
    image_duration = 10  # Duration for each image in seconds
    total_duration = get_mp3_duration("script_audio.mp3")  # Total duration of the audio in seconds
    output_file = "slideshow.mp4"  # Output file name
    resolution = (1280, 720)  # Default resolution

    create_slideshow(output_folder, image_duration, total_duration, output_file, resolution)


def create_slideshow(images_folder, image_duration, total_duration, output_file, resolution):
    # Get a list of image files
    image_files = [os.path.join(images_folder, file) for file in os.listdir(images_folder) if file.endswith('.jpg')]

    # Generate a temporary file to store the list of image files
    image_list_file = "image_list.txt"
    with open(image_list_file, 'w') as f:
        for image_file in image_files:
            f.write(f"file '{image_file}'\n")

    # Create slideshow from images using FFmpeg
    subprocess.run([
        'ffmpeg',
        '-y',  # Overwrite output file if it already exists
        '-f', 'concat',
        '-safe', '0',
        '-i', image_list_file,
        '-vf', f'fps={1/image_duration},scale={resolution[0]}:{resolution[1]},format=yuv420p',
        '-c:v', 'libx264',
        '-t', f'{total_duration}',
        '-movflags', 'faststart',
        '-s', f'{resolution[0]}x{resolution[1]}',
        output_file
    ], check=True)

    # Clean up the temporary image list file
    os.remove(image_list_file)


def get_mp3_duration(file_path):
    audio = MP3(file_path)
    duration_sec = audio.info.length
    return duration_sec


if __name__ == "__main__":
    main()
