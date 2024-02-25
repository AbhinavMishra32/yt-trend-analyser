import os
from moviepy.editor import ImageClip, concatenate_videoclips

def generate_slide(image_path, duration, zoom_scale):
    """Generate a slide with Ken Burns effect."""
    clip = ImageClip(image_path, duration=duration)
    zoom_in = clip.resize(lambda t: zoom_scale(t))
    zoom_out = clip.resize(lambda t: zoom_scale(1 - t))
    return concatenate_videoclips([zoom_in.crossfadein(0.5), zoom_out.crossfadein(0.5)], method="compose")


def create_slideshow(images_folder, image_duration, total_duration):
    """Create a slideshow from images in a folder."""
    clips = []
    images = sorted(os.listdir(images_folder))
    for image in images:
        image_path = os.path.join(images_folder, image)
        slide = generate_slide(image_path, image_duration, lambda t: 1.3 + 0.3 * t)
        clips.append(slide.set_duration(image_duration))
        if sum([clip.duration for clip in clips]) >= total_duration:
            break
    return concatenate_videoclips(clips)

if __name__ == "__main__":
    # Folder containing images
    images_folder = "/Users/abhinavmishra/Documents/Automated_vids/images/vid_3"
    
    # Duration for each image in seconds
    image_duration = 5
    
    # Total duration of the video in seconds
    total_duration = 20
    
    # Create slideshow
    slideshow = create_slideshow(images_folder, image_duration, total_duration)
    
    # Export slideshow to a file
    output_file = "/Users/abhinavmishra/Documents/Automated_vids/slideshow.mp4"
    slideshow.write_videofile(output_file, fps=24)
