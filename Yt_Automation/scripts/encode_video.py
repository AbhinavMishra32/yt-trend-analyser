import subprocess

def reencode_video(input_video, reference_video, output_video):
    # Get properties of the reference video
    ffprobe_command = [
        'ffprobe',
        '-v', 'error',
        '-select_streams', 'v:0',
        '-show_entries', 'stream=codec_name,width,height,r_frame_rate',
        '-of', 'default=noprint_wrappers=1:nokey=1',
        reference_video
    ]
    reference_properties = subprocess.check_output(ffprobe_command).decode().split('\n')
    codec_name, width, height, frame_rate = reference_properties[:4]

    # Re-encode the input video to match the properties of the reference video
    ffmpeg_command = [
        'ffmpeg',
        '-i', input_video,
        '-c:v', 'libx264',  # Use libx264 codec
        '-vf', f'scale={width}:{height}',
        '-r', frame_rate,
        output_video
    ]
    subprocess.run(ffmpeg_command, check=True)

def main():
    input_video = 'final_video.mp4'
    reference_video = 'sub_video.mp4'
    output_video = 'final_video_encoded.mp4'
    reencode_video(input_video, reference_video, output_video)

if __name__ == "__main__":
    main()
