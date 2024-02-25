import cv2
import os
import youtube_dl

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
        ydl_opts = {'outtmpl': 'temp_video.mp4'}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_path])
        video_path = 'temp_video.mp4'

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
    if video_path == 'temp_video.mp4':
        os.remove('temp_video.mp4')

# Example usage:
# video_path = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # YouTube video link
video_path = "Shaitaan Trailer | Ajay Devgn, R Madhavan, Jyotika | Jio Studios, Devgn Films, Panorama Studios.mp4"  # Path to local video file
output_folder = "output_frames"
interval = 10  # Interval in seconds
extract_frames(video_path, output_folder, interval)
