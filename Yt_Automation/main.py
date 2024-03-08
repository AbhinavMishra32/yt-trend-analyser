import subprocess

movie_name = "Ra one 2 2024"
video_url = "https://www.youtube.com/watch?v=-05HzY1erR0"
images_count = 20

# Define the pipeline steps with step numbers
pipeline_steps = {
    1: ["python3", "scripts/gemini_script.py", movie_name],
    2: ["python3", "scripts/eleven_labs_api.py"],
    3: ["python3", "scripts/extract_frames.py", "'"+video_url+"'", images_count],
    4: ["python3", "scripts/slideshow_maker.py"],
    5: ["python3", "scripts/combine_audio_video.py"],
    6: ["python3", "scripts/combine_videos_ffmpeg.py"],
    7: ["python3", "scripts/combine_intro.py"],
    # 8: ["python3", "scripts/youtube_upload.py", movie_name],
}

# Select the start of the pipeline
start_step = 7  # Change this to select a different start step

for step in range(start_step, len(pipeline_steps) + 1):
    print(subprocess.check_output(pipeline_steps[step]).decode())