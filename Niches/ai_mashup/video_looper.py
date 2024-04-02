import subprocess
import os

# Load video file
video_path = "sources/raw_loop_video.mp4"

# Get audio duration using ffprobe
audio_path = "mashup.wav"
ffprobe_cmd = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', audio_path]
audio_duration = float(subprocess.check_output(ffprobe_cmd))

# Create reversed video
reversed_video_path = "reversed_video.mp4"
ffmpeg_cmd = ['ffmpeg', '-i', video_path, '-vf', 'reverse', '-c', 'libx264', '-pix_fmt', 'yuv420p', reversed_video_path]
subprocess.run(ffmpeg_cmd)

# Concatenate original and reversed videos
concat_video_path = "concat_video.mp4"
with open('concat_list.txt', 'w') as f:
    f.write(f"file '{video_path}'\nfile '{reversed_video_path}'")
ffmpeg_cmd = ['ffmpeg', '-f', 'concat', '-safe', '0', '-i', 'concat_list.txt', '-c', 'copy', concat_video_path]
subprocess.run(ffmpeg_cmd)
os.remove('concat_list.txt')

# Calculate desired length and number of repeats
video_duration = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', concat_video_path]))
repeats_needed = int(audio_duration / video_duration)

# Repeat concatenated video
repeated_video_path = "repeated_video.mp4"
with open('repeated_list.txt', 'w') as f:
    for _ in range(repeats_needed):
        f.write(f"file '{concat_video_path}'\n")
ffmpeg_cmd = ['ffmpeg', '-f', 'concat', '-safe', '0', '-i', 'repeated_list.txt', '-c', 'copy', repeated_video_path]
subprocess.run(ffmpeg_cmd)
os.remove('repeated_list.txt')

# Trim repeated video to match audio duration
trimmed_video_path = "trimmed_video.mp4"
ffmpeg_cmd = ['ffmpeg', '-i', repeated_video_path, '-t', str(audio_duration), '-c', 'copy', trimmed_video_path]
subprocess.run(ffmpeg_cmd)

# Combine the trimmed video and audio
output_path = "mashup_video.mp4"
ffmpeg_cmd = ['ffmpeg', '-i', trimmed_video_path, '-i', audio_path, '-c', 'copy', '-map', '0:v:0', '-map', '1:a:0', output_path]
subprocess.run(ffmpeg_cmd)

# Clean up temporary files
os.remove(reversed_video_path)
os.remove(concat_video_path)
os.remove(repeated_video_path)
os.remove(trimmed_video_path)

print(f"Video created successfully at {output_path}")