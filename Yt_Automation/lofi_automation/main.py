import subprocess
import os

pipeline_steps = {
    1: ["python3.12", "lofi_maker/spotify_downloader.py"],
    2: ["python3.12", "lofi_maker/drakify/lofi_generator.py"],
    3: ["python3", "lofi_maker/aud_vid_ffmpeg.py"],
}

# Select the start of the pipeline
start_step = 1  # Change this to select a different start step

# Change the working directory to the directory containing the scripts
# os.chdir('/Users/abhinavmishra/Coding/yt-trend-analyser/Yt_Automation/lofi_automation/lofi_maker')

for step in range(start_step, len(pipeline_steps) + 1):
    process = subprocess.Popen(
        pipeline_steps[step],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,  # Merge stderr with stdout
        universal_newlines=True,  # Decode output to text
    )
    for line in process.stdout:
        print(line, end='')  # Print each line of output
    process.wait()  # Wait for subprocess to finish
