import cv2
import os
import tempfile
from pytube import YouTube
import shutil

def download_youtube_video(video_url, output_path):
    """
    Downloads a YouTube video.

    Parameters:
        video_url (str): URL of the YouTube video.
        output_path (str): Path where the video will be saved.
    """
    yt = YouTube(video_url)
    yt.streams.filter(file_extension='mp4').first().download(output_path)

def extract_frames(video_path, output_folder, interval):
    """
    Extracts still frames from a video at specified intervals.

    Parameters:
        video_path (str): Path to the input video file or YouTube video link.
        output_folder (str): Path to the folder where extracted frames will be saved.
        interval (int): Interval (in seconds) between extracted frames.
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

    # Remove temporary video file if it was downloaded
    if video_path == os.path.join(output_folder, 'temp_video.mp4'):
        os.remove(os.path.join(output_folder, 'temp_video.mp4'))

# Example usage:
video_path = "https://www.youtube.com/watch?v=uJMCNJP2ipI"  # YouTube video link
# Or video_path = "local_video.mp4"  # Path to local video file
output_folder = "output_frames"
interval = 10  # Interval in seconds
extract_frames(video_path, output_folder, interval)
