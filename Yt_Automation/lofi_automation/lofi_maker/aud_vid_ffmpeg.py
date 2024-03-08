import subprocess

def combine_image_audio(image_path, audio_path, output_path, resolution=(1920, 1080), fps=30):
    # Get duration of audio using ffprobe
    ffprobe_cmd = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', audio_path]
    duration = float(subprocess.check_output(ffprobe_cmd))

    # Use ffmpeg to create video
    ffmpeg_cmd = ['ffmpeg', '-loop', '1', '-i', image_path, '-i', audio_path, '-c:v', 'libx264', '-t', str(duration), '-vf', 'scale={}:{}'.format(resolution[0], resolution[1]), '-r', str(fps), '-pix_fmt', 'yuv420p', output_path]
    subprocess.run(ffmpeg_cmd)

if __name__ == "__main__":
    # Paths to input files
    image_path = "images/lofi_cover.jpg"
    audio_path = "drakify/source/songs/lofi_songs.wav"

    # Output video file path
    output_path = "output_video.mp4"

    # Combine image and audio with custom resolution and FPS
    combine_image_audio(image_path, audio_path, output_path, resolution=(1920, 1080), fps=24)

    print("Video created successfully at", output_path)
