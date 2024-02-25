from moviepy.editor import ImageSequenceClip
import os
import random

# Function to generate random duration between specified range
def generate_random_duration():
    return random.randint(7800, 9000)  # Random duration between 2 hours 10 minutes and 2 hours 30 minutes

# Function to generate random zoom effect
def generate_random_zoom_effect():
    zoom_options = [(0.8, 1.2), (0.9, 1.3), (1.0, 1.4)]  # Zoom ranges
    return random.choice(zoom_options)

# Specify input image folder and output video path
image_folder = "/Users/abhinavmishra/Documents/Automated_vids/images/vid_3"
output_video = "/Users/abhinavmishra/Documents/automated_video.mp4"

# Get list of image files
image_files = [os.path.join(image_folder, file) for file in os.listdir(image_folder) if file.endswith('.jpg')]

# Generate random duration and zoom effect
# duration = generate_random_duration()
duration = 3
zoom_start, zoom_end = generate_random_zoom_effect()

# Specify desired resolution
width, height = 1920, 1080  # Example resolution (1920x1080)

# Create ImageSequenceClip from images
clip = ImageSequenceClip(image_files, fps=1/duration, load_images=True)

# Resize each frame to the desired resolution
clip = clip.resize((width, height))

# Write video file
clip.write_videofile(output_video, codec='libx264', fps=24)
