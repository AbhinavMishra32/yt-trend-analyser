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
output_file = 'final_video.mp4'

concatenate_videos(input_list_file, output_file)
