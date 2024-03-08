import subprocess

def concatenate_videos(input_list_file, output_file):
    # Generate the FFmpeg command
    ffmpeg_command = [
        'ffmpeg',
        '-y',  # Overwrite output files without asking
        '-f', 'concat',  # Use the concat demuxer
        '-safe', '0',  # Allow absolute paths in the input file
        '-i', input_list_file,
        '-c', 'copy',  # Copy audio and video codecs
        output_file
    ]
    
    # Run the FFmpeg command
    subprocess.run(ffmpeg_command, check=True)
# Example usage:
input_list_file = 'input_list.txt'
#if input_list_file does not exist, create it
with open(input_list_file, 'w') as f:
    f.write("file 'video_intro.mp4'\n")
    f.write("file 'combined_video.mp4'\n")

output_file = 'final_video_1111.mp4'

concatenate_videos(input_list_file, output_file)
print("Videos concatenated successfully at", output_file)