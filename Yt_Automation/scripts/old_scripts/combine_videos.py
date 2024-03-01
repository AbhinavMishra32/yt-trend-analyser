import os
import random
from moviepy.editor import VideoFileClip, concatenate_videoclips

def combine_videos(video_file, max_duration):
    # Load the video clip
    clip = VideoFileClip(video_file)
    
    # Determine how many times the clip needs to be repeated to reach or exceed max_duration
    num_repeats = int(max_duration / clip.duration) + 1
    
    # Repeat the clip
    video_clips = [clip] * num_repeats
    
    # Concatenate the repeated clips
    final_clip = concatenate_videoclips(video_clips)
    
    # Trim the final clip to the desired duration
    final_clip = final_clip.subclip(0, max_duration)
    
    return final_clip

def main():
    # Input video file
    video_file = "sub_video.mp4"
    
    # Maximum duration for the final video (between 1 hour 30 minutes and 2 hours 20 minutes)
    max_duration = random.randint(5400, 8400)  # 5400 seconds = 1.5 hours, 8400 seconds = 2.333 hours
    
    # Combine the videos
    final_clip = combine_videos(video_file, max_duration)
    
    # Export the final video
    final_clip.write_videofile("combined_video.mp4")

if __name__ == "__main__":
    main()
