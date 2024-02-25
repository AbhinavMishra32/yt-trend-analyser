import moviepy.editor as mp
import math
from PIL import Image
import numpy
import os 

def zoom_in_effect(clip, zoom_ratio=0.04):
    def effect(get_frame, t):
        img = Image.fromarray(get_frame(t))
        base_size = img.size

        new_size = [
            math.ceil(img.size[0] * (1 + (zoom_ratio * t))),
            math.ceil(img.size[1] * (1 + (zoom_ratio * t)))
        ]

        # The new dimensions must be even.
        new_size[0] = new_size[0] + (new_size[0] % 2)
        new_size[1] = new_size[1] + (new_size[1] % 2)

        img = img.resize(new_size, Image.LANCZOS)

        x = math.ceil((new_size[0] - base_size[0]) / 2)
        y = math.ceil((new_size[1] - base_size[1]) / 2)

        img = img.crop([
            x, y, new_size[0] - x, new_size[1] - y
        ]).resize(base_size, Image.LANCZOS)

        result = numpy.array(img)
        img.close()

        return result

    return clip.fl(effect)


def create_slideshow(images_folder, image_duration, total_duration):
    """Create a slideshow from images in a folder."""
    clips = []
    images = [f for f in os.listdir(images_folder) if not f.startswith('.')]  # Filter out hidden files
    for image in images:
        image_path = os.path.join(images_folder, image)

        # Load as a MoviePy clip
        clip = mp.ImageClip(image_path).set_duration(image_duration)  

        # Apply the zoom effect
        slide = zoom_in_effect(clip, zoom_ratio=0.04) 

        clips.append(slide)
        if sum([clip.duration for clip in clips]) >= total_duration:
            break
    return mp.concatenate_videoclips(clips)

# Folder containing images
images_folder = "/Users/abhinavmishra/Documents/Automated_vids/images/vid_3"
    
# Duration for each image in seconds
image_duration = 10
    
# Total duration of the video in seconds
total_duration = 30
    
# Create slideshow
slideshow = create_slideshow(images_folder, image_duration, total_duration)
    
# Export slideshow to a file
output_file = "/Users/abhinavmishra/Documents/Automated_vids/slideshow.mp4"
slideshow.write_videofile(output_file, fps=24)
