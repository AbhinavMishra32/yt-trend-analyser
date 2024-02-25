import subprocess

# Create script of video
subprocess.call(["python3", "gemini_script.py"])

# Create audio for the script
subprocess.call(["python3", "eleven_labs_api.py"])

# Create images from video
subprocess.call(["python3", "extract_frames.py"])

# Create slideshow from images
subprocess.call(["python3", "slideshow_maker.py"])

# Combine audio and video
subprocess.call(["python3", "combine_audio_video.py"])
