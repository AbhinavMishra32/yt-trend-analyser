from moviepy.editor import ImageSequenceClip
import os

# Specify input image folder and output video path
image_folder = "/Users/abhinavmishra/Documents/Automated_vids/images/vid_3"
output_video = "/Users/abhinavmishra/Documents/automated_video.mp4"

# Get list of image files
image_files = [os.path.join(image_folder, file) for file in os.listdir(image_folder) if file.endswith('.jpg')]

# Specify individual slide duration (in seconds)
slide_duration = 10  # Default slide duration

# Calculate the number of frames per second based on total duration and number of images
num_frames = len(image_files)
fps = num_frames / slide_duration

# Specify desired resolution
width, height = 1920, 1080  # Example resolution (1920x1080)

# Create ImageSequenceClip from images
clip = ImageSequenceClip(image_files, fps=fps, load_images=True)

# Define function to apply zoom effect to each frame
def apply_zoom(frame):
    zoom_factor_in = 1.8  # Zoom in to 180%
    zoom_factor_out = 1.2  # Zoom out to 120%
    zoomed_in_frame = frame.resize((int(width * zoom_factor_in), int(height * zoom_factor_in)))
    return zoomed_in_frame.resize((width, height))  # Resize back to original size after zooming

# Apply zoom effect to each frame
clip = clip.fl_image(apply_zoom)

# Write video file
clip.write_videofile(output_video, codec='libx264', fps=fps)
