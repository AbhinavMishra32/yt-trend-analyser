import subprocess

# Create script of video
print(subprocess.check_output(["python3", "scripts/gemini_script.py"]).decode())

# Create audio for the script
print(subprocess.check_output(["python3", "scripts/eleven_labs_api.py"]).decode())

# Create images from video
print(subprocess.check_output(["python3", "scripts/extract_frames.py"]).decode())

# Create slideshow from images
print(subprocess.check_output(["python3", "scripts/slideshow_maker.py"]).decode())

# Combine audio and video
print(subprocess.check_output(["python3", "scripts/combine_audio_video.py"]).decode())