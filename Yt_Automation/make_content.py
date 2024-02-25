"""
Gets script from Google Gemini Pro and creates a slideshow from the video frames, connects trailer to the slideshow and exports the final video.
"""
import cv2
import os
import moviepy.editor as mp
import math
from PIL import Image
import numpy

def extract_frames(video_path, output_folder, interval):
    """
    Extracts still frames from a video at specified intervals.

    Parameters:
        video_path (str): Path to the input video file.
        output_folder (str): Path to the folder where extracted frames will be saved.
        interval (int): Interval (in seconds) between extracted frames.
    """
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Open the video file
    video_capture = cv2.VideoCapture(video_path)
    fps = video_capture.get(cv2.CAP_PROP_FPS)
    frame_count = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))

    # Calculate frame interval based on the desired time interval
    frame_interval = int(interval * fps)

    # Read and save frames at specified intervals
    frame_number = 0
    while True:
        # Set frame position
        video_capture.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        ret, frame = video_capture.read()
        if not ret:
            break

        # Save frame
        output_path = os.path.join(output_folder, f"frame_{frame_number}.jpg")
        cv2.imwrite(output_path, frame)

        # Move to the next frame based on the interval
        frame_number += frame_interval
        if frame_number >= frame_count:
            break

    # Release video capture object
    video_capture.release()

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


def create_slideshow(images_folder, image_duration, total_duration):
    """Create a slideshow from images in a folder."""
    clips = []
    images = [f for f in os.listdir(images_folder) if not f.startswith('.')]  # Filter out hidden files
    total_duration_remaining = total_duration
    while total_duration_remaining > 0:
        for image in images:
            image_path = os.path.join(images_folder, image)

            # Load as a MoviePy clip
            clip = mp.ImageClip(image_path).set_duration(image_duration)  

            # Apply the zoom effect
            slide = zoom_in_effect(clip, zoom_ratio=0.04) 

            clips.append(slide)
            total_duration_remaining -= image_duration
            if total_duration_remaining <= 0:
                break
    
    return mp.concatenate_videoclips(clips)

# Parameters
video_path = "Shaitaan Trailer | Ajay Devgn, R Madhavan, Jyotika | Jio Studios, Devgn Films, Panorama Studios.mp4"
output_folder = "output_frames"
interval = 10  # Interval in seconds
images_folder = "output_frames"  # Folder containing extracted frames
image_duration = 10  # Duration for each image in seconds
total_duration = 20  # Total duration of the video in seconds
output_file = "slideshow.mp4"  # Output file name
resolution = (1280, 720)  # Default resolution

# Extract frames from the video
extract_frames(video_path, output_folder, interval)

# Create slideshow from extracted frames
slideshow = create_slideshow(images_folder, image_duration, total_duration)

# Set video resolution
slideshow = slideshow.resize(resolution)

# Export slideshow to a file with specified codec, threads, and resolution
slideshow.write_videofile(output_file, fps=24, codec='libx264', threads=4, verbose=False)
