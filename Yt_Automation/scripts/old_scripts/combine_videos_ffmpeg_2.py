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
        # Write the start_part_fixed.mp4 video first
        f.write(f"file 'start_part_fixed.mp4'\n")
        # Write the input video for repetition
        for _ in range(repeat_count):
            f.write(f"file '{input_video}'\n")
    
    # Generate a silent audio track for the start_part_fixed.mp4 video
    subprocess.run([
        'ffmpeg',
        '-y',
        '-i', 'start_part_fixed.mp4',
        '-f', 'lavfi',
        '-i', 'aevalsrc=0',
        '-shortest',
        '-c:v', 'copy',
        '-c:a', 'aac',
        '-b:a', '160k',
        '-strict', 'experimental',
        'new_start_part.mp4'
    ], check=True)

    # Concatenate the input videos including the silent audio track
    subprocess.run([
        'ffmpeg',
        '-y',
        '-f', 'concat',
        '-safe', '0',
        '-i', input_list_file,
        '-c:v', 'copy',
        '-c:a', 'aac',
        '-b:a', '160k',
        '-strict', 'experimental',
        output_video
    ], check=True)
    
    # Remove the temporary input list file and the generated silent audio track
    os.remove(input_list_file)
    os.remove('new_start_part.mp4')

def get_video_duration(video_file):
    # Check if the video file exists
    if not os.path.exists(video_file):
        print(f"Video file '{video_file}' not found.")
        return None

    # Run ffprobe to get the duration of the video
    result = subprocess.run([
        'ffprobe',
        '-v', 'error',
        '-show_entries', 'format=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1',
        video_file
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Check if ffprobe encountered an error
    if result.returncode != 0:
        print("Error running ffprobe:", result.stderr.decode())
        return None

    # Parse the output to get the duration
    duration = float(result.stdout)
    return duration



def main():
    # Input video files
    sub_video = "sub_video_fixed.mp4"

    # Output video file
    output_video = "combined_video.mp4"
    
    # Minimum and maximum duration for the final video (in seconds)
    min_duration = 6400 # 1.777 hours
    max_duration = 8400  # 2.333 hours
    
    # Repeat the input video to create the final video
    repeat_video(sub_video, output_video, min_duration, max_duration)

if __name__ == "__main__":
    main()
