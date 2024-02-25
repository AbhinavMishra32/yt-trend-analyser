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
                math.ceil(img.size[0] / (1 + (zoom_ratio * t))), 
                math.ceil(img.size[1] / (1 + (zoom_ratio * t))) 
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
    clips = []
    images = [f for f in os.listdir(images_folder) if not f.startswith('.')]
    images.reverse()  # Reverse the image order

    for image in images:
        image_path = os.path.join(images_folder, image)
        clip = mp.ImageClip(image_path).set_duration(image_duration)  
        slide = zoom_in_effect(clip, zoom_ratio=0.04) 
        clips.append(slide)
        if sum([clip.duration for clip in clips]) >= total_duration:
            break
    
    slideshow = mp.concatenate_videoclips(clips)

    # Reverse the video during export
    output_file = "/Users/abhinavmishra/Documents/Automated_vids/reversed_slideshow.mp4"  
    slideshow.write_videofile(output_file, fps=24, codec='libx264', audio=False, 
                               logger=None, preset='ultrafast', threads=4, ffmpeg_params=["-vf", "reverse"]) 

# Folder containing images
images_folder = "/Users/abhinavmishra/Documents/Automated_vids/images/vid_3"
    
# Duration for each image in seconds
image_duration = 5
    
# Total duration of the video in seconds
total_duration = 20 
