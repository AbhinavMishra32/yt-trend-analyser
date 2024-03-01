import sys
import subprocess

movie_name = "Captain Miller"
video_url = "https://www.youtube.com/watch?v=a1HTHoHI5qE"

# Define the pipeline steps with step numbers and arguments
pipeline_steps = [
    ["python3", "scripts/gemini_script.py", movie_name],  # Replace "arg1", "arg2", ... with your arguments
    ["python3", "scripts/eleven_labs_api.py"],
    ["python3", "scripts/extract_frames.py", video_url],
    ["python3", "scripts/slideshow_maker.py"],
    ["python3", "scripts/combine_audio_video.py"],
    ["python3", "scripts/combine_videos_ffmpeg.py"],
    ["python3", "scripts/youtube_upload.py", movie_name],
]

# Select the start of the pipeline
start_step = 5  # Change this to select a different start step

# Execute the pipeline steps starting from the selected step
for step, args in enumerate(pipeline_steps[start_step - 1:], start=start_step):
    print(f"Step {step}: Executing {' '.join(args)}")
    process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if stdout:
        print(stdout.decode())
    if stderr:
        print(stderr.decode())
