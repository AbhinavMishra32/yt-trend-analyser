import cv2
import os
import tempfile
from pytube import YouTube
import shutil
import sys
import requests

def download_youtube_video(video_url, output_path):
    """
    Downloads a YouTube video.

    Parameters:
        video_url (str): URL of the YouTube video.
        output_path (str): Path where the video will be saved.
    """
    yt = YouTube(video_url)
    yt.streams.filter(file_extension='mp4').get_highest_resolution().download(output_path) #type: ignore

def extract_frames(video_path, output_folder, images_count):
    """
    Extracts still frames from a video at specified intervals.

    Parameters:
        video_path (str): Path to the input video file or YouTube video link.
        output_folder (str): Path to the folder where extracted frames will be saved.
        images_count (int): Number of frames/images to extract from the video.
    """
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    if video_path.startswith("http"):  # If video_path is a YouTube link
        # Download YouTube video
        with tempfile.TemporaryDirectory() as temp_dir:
            download_youtube_video(video_path, temp_dir)
            temp_video_path = os.path.join(temp_dir, os.listdir(temp_dir)[0])
            shutil.copy(temp_video_path, os.path.join(output_folder, 'temp_video.mp4'))
            video_path = os.path.join(output_folder, 'temp_video.mp4')

    # Open the video file
    video_capture = cv2.VideoCapture(video_path)
    fps = video_capture.get(cv2.CAP_PROP_FPS)
    frame_count = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
    video_length = frame_count / fps

    # Calculate the interval based on the desired time interval between frames
    interval_time = video_length / images_count

    # Calculate the frame interval based on the video's frame rate
    interval_frame = int(interval_time * fps)

    # Read and save frames at specified intervals
    frame_number = 0
    images_saved = 0
    while images_saved < images_count:
        # Set frame position
        video_capture.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        ret, frame = video_capture.read()
        if not ret:
            break

        # Save frame
        output_path = os.path.join(output_folder, f"frame_{frame_number}.jpg")
        cv2.imwrite(output_path, frame)
        images_saved += 1

        # Move to the next frame based on the interval
        frame_number += interval_frame

    # Release video capture object
    video_capture.release()

    # Remove temporary video file if it was downloaded
    if video_path == os.path.join(output_folder, 'temp_video.mp4'):
        os.remove(os.path.join(output_folder, 'temp_video.mp4'))

def save_video_title(video_url, output_path):
    """
    Saves the title of a YouTube video to a .txt file.

    Parameters:
        video_url (str): URL of the YouTube video.
        output_path (str): Path where the title will be saved.
    """
    yt = YouTube(video_url)
    video_title = yt.title
    with open(output_path, "w") as file:
        file.write(video_title)

def download_thumbnail(video_url, output_folder):
    """
    Downloads the thumbnail of a YouTube video.

    Parameters:
        video_url (str): URL of the YouTube video.
        output_folder (str): Path to the folder where the thumbnail will be saved.
    """
    yt = YouTube(video_url)
    thumbnail_url = yt.thumbnail_url
    thumbnail_path = os.path.join(output_folder, "thumbnail.jpg")
    
    # Create the thumbnail folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    with open(thumbnail_path, "wb") as thumbnail_file:
        thumbnail_file.write(requests.get(thumbnail_url).content)

if __name__ == "__main__":
    # if len(sys.argv) < 3:
    #     print("Please provide the video path and images_count as command-line arguments.")
    #     sys.exit(1)

    # Example usage:
    video_path = sys.argv[1]  # YouTube video link or path to local video file
    # video_path = "trailer.mp4"  # Path to local video file
    output_folder = "output_frames"
    thumbnail_folder = "output_frames/thumbnail"
    title_file_path = "output_frames/thumbnail/video_title.txt"

    images_count = int(sys.argv[2])  # Number of frames/images to extract from the video
    extract_frames(video_path, output_folder, images_count)
    # download_thumbnail(video_path, thumbnail_folder)
    # save_video_title(video_path, title_file_path)
