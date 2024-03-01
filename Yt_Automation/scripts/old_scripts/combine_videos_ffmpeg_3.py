import subprocess
import os

def encode_video(input_video, output_video, codec_params):
    subprocess.run([
        'ffmpeg',
        '-i', input_video,
        *codec_params,
        output_video
    ], check=True)

def concatenate_videos(input_videos, output_video):
    with open('input_list.txt', 'w') as f:
        for video in input_videos:
            f.write(f"file '{video}'\n")

    subprocess.run([
        'ffmpeg',
        '-y',
        '-f', 'concat',
        '-safe', '0',
        '-i', 'input_list.txt',
        '-c', 'copy',
        output_video
    ], check=True)

def main():
    start_part_video = "start_part.mp4"
    combined_video = "combined_video.mp4"
    final_video = "final_video.mp4"

    # Check if encoding is needed for start_part.mp4
    encoding_needed = False
    codec_params = []

    try:
        # Check video properties
        start_part_props = subprocess.check_output(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=codec_name,width,height', '-of', 'default=noprint_wrappers=1', start_part_video]).decode()

        combined_props = subprocess.check_output(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=codec_name,width,height', '-of', 'default=noprint_wrappers=1', combined_video]).decode()

        if start_part_props != combined_props:
            # Encoding needed to match properties
            encoding_needed = True
            codec_params = ['-vf', f'scale={combined_props.split("width=")[1].split(",")[0]}:{combined_props.split("height=")[1].split(",")[0]}']

    except subprocess.CalledProcessError as e:
        print("Error:", e.output)
        return

    # Encode start_part.mp4 if necessary
    if encoding_needed:
        encoded_start_part = "encoded_start_part.mp4"
        encode_video(start_part_video, encoded_start_part, codec_params)
        start_part_video = encoded_start_part

    # Concatenate videos
    concatenate_videos([start_part_video, combined_video], final_video)

    # Cleanup
    if encoding_needed:
        os.remove(encoded_start_part)
    os.remove('input_list.txt')

if __name__ == "__main__":
    main()
