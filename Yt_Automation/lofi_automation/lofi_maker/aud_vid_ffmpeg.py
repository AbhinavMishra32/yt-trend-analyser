import subprocess

def render_short_video_clip(image_path, output_path, duration, resolution=(1920, 1080), fps=30):
    # Use ffmpeg to create a short video clip from the image
    ffmpeg_cmd = ['ffmpeg', '-loop', '1', '-i', image_path, '-c:v', 'libx264', '-t', str(duration), '-vf', 'scale={}:{}'.format(resolution[0], resolution[1]), '-r', str(fps), '-pix_fmt', 'yuv420p', output_path]
    subprocess.run(ffmpeg_cmd)

def combine_video_audio(video_path, audio_path, output_path):
    # Use ffmpeg to combine short video clip and audio
    ffmpeg_cmd = ['ffmpeg', '-i', video_path, '-i', audio_path, '-c:v', 'copy', '-c:a', 'aac', '-strict', 'experimental', '-map', '0:v:0', '-map', '1:a:0', '-shortest', output_path]
    subprocess.run(ffmpeg_cmd)

if __name__ == "__main__":
    # Paths to input files
    image_path = "images/lofi_cover.jpg"
    audio_path = "drakify/source/songs/lofi_songs.wav"

    # Output video file path
    output_path = "output_video.mp4"

    # Duration of the audio file
    ffprobe_cmd = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', audio_path]
    audio_duration = float(subprocess.check_output(ffprobe_cmd))

    # Duration of the short video clip (in seconds)
    short_video_duration = 1  # Example: 10 seconds

    # Render a short video clip from the image
    render_short_video_clip(image_path, "short_video.mp4", short_video_duration)

    # Calculate the number of times the short video clip needs to be repeated to match the audio duration
    num_repeats = int(audio_duration / short_video_duration) + 1

    # Use ffmpeg to concatenate short video clips to match the audio duration
    ffmpeg_concat_cmd = ['ffmpeg', '-stream_loop', str(num_repeats), '-i', 'short_video.mp4', '-c', 'copy', 'concatenated_video.mp4']
    subprocess.run(ffmpeg_concat_cmd)

    # Combine the concatenated video and audio
    combine_video_audio("concatenated_video.mp4", audio_path, output_path)

    # Delete temporary files
    subprocess.run(['rm', 'short_video.mp4', 'concatenated_video.mp4'])

    print("Video created successfully at", output_path)
