import subprocess

movie_name = "Razakar, Cast - Gudur Narayana Reddy | Yata Satyanarayana | Bheems Ceciroleo"
video_url = "https://www.youtube.com/watch?v=q1lM6LF6Xlk&pp=ygUUcmF6YWthciBtdm9pZSB0cmFpZXI%3D"
images_count = 28

"""
Run from Yt_Automation directory
"""

# Define the pipeline steps with step numbers
pipeline_steps = {
    1: ["python3.12", "scripts/gemini_script.py", movie_name],
    2: ["python3.12", "scripts/elevenlabs_auto.py"], # of scripts/elevenlabs_auto.py
    3: ["python3.12", "scripts/extract_frames.py", "'"+video_url+"'", images_count],
    4: ["python3.12", "scripts/slideshow_maker.py"],
    5: ["python3.12", "scripts/combine_audio_video.py"],
    6: ["python3.12", "scripts/combine_videos_ffmpeg.py"],
    7: ["python3.12", "scripts/combine_intro.py"],
    # 8: ["python3", "scripts/youtube_upload.py", movie_name],
}

# Select the start of the pipeline
start_step = 5  # Change this to select a different start step

for step in range(start_step, len(pipeline_steps) + 1):
    print(subprocess.check_output(pipeline_steps[step]).decode())