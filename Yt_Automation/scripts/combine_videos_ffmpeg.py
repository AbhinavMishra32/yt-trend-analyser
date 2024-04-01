import random
import subprocess
import os

def repeat_video(input_video, output_video, min_duration, max_duration):
    # Generate a random duration within the specified range
    target_duration = random.randint(min_duration, max_duration)
    
    # Calculate the number of times to repeat the input video
    input_duration = get_video_duration(input_video)
    repeat_count = max(1, int(target_duration / input_duration))
    
    # Create a temporary text file with the list of input videos
    input_list_file = "input_list.txt"
    with open(input_list_file, "w") as f:
        for _ in range(repeat_count):
            f.write(f"file '{input_video}'\n")
    
    # Run ffmpeg to concatenate the input videos
    subprocess.run([
        'ffmpeg',
        '-y',  # Overwrite output file if it already exists
        '-f', 'concat',
        '-safe', '0',
        '-i', input_list_file,
        '-c', 'copy',
        output_video
    ], check=True)
    
    # Remove the temporary input list file
    os.remove(input_list_file)

def get_video_duration(video_file):
    # Run ffprobe to get the duration of the video
    result = subprocess.run([
        'ffprobe',
        '-v', 'error',
        '-show_entries', 'format=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1',
        video_file
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Parse the output to get the duration
    duration = float(result.stdout)
    return duration

def main():
    # Input video file
    input_video = "sub_video.mp4"
    
    # Output video file
    output_video = "combined_video.mp4"
    
    # Minimum and maximum duration for the final video (in seconds)
    min_duration = 7900 # 2.194 hours
    max_duration = 11500 # 3.194 hours
    
    # Repeat the input video to create the final video
    repeat_video(input_video, output_video, min_duration, max_duration)

if __name__ == "__main__":
    main()
