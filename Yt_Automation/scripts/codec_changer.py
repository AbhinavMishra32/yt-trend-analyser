from moviepy.editor import VideoFileClip, concatenate_videoclips
import os

def concatenate_videos(input_videos, output_file):
    # Load video clips
    clips = [VideoFileClip(video) for video in input_videos]
    
    # Concatenate video clips
    final_clip = concatenate_videoclips(clips, method="compose")
    
    # Export final video with ultrafast preset and multithreading
    final_clip.write_videofile(output_file, codec='libx264', fps=final_clip.fps,
                                preset='ultrafast', threads=os.cpu_count())
    
    # Close video clips
    for clip in clips:
        clip.close()

# List of input videos
input_videos = ['start_part.mp4', 'combined_video.mp4']

# Output file
output_file = 'concatenated_video.mp4'

# Concatenate videos
concatenate_videos(input_videos, output_file)
