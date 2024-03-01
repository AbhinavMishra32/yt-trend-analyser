from moviepy.editor import *

# Function to create a slideshow
def create_slideshow(output_file):
    # Create clips with colorful backgrounds
    clip1 = ColorClip((800, 600), color=(255, 0, 0)).set_duration(3)
    clip2 = ColorClip((800, 600), color=(0, 255, 0)).set_duration(3)
    clip3 = ColorClip((800, 600), color=(0, 0, 255)).set_duration(3)

    # Concatenate clips to create slideshow
    slideshow = concatenate_videoclips([clip1, clip2, clip3])

    # Export slideshow as mp4 file
    slideshow.write_videofile(output_file, fps=24)

# Output file name
output_file = "slideshow_demo.mp4"

# Create slideshow
create_slideshow(output_file)
