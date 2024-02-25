from moviepy.editor import ImageClip
import time

def zoom_scale(t):
    return 1.5 + 1.0 * t  # Increased zoom speed

def zoom(t):
    factor = zoom_scale(t) 
    clip = ImageClip('/Users/abhinavmishra/Documents/Automated_vids/images/vid_3/frame_1680.jpg', duration=2)
    scaled_w = clip.w * factor 
    scaled_h = clip.h * factor
    x_offset = (scaled_w - clip.w) / 2 
    y_offset = (scaled_h - clip.h) / 2 
    return clip.resize(factor).set_position(('center', 'center')).crop(y1=y_offset, x1=x_offset, width=scaled_w, height=scaled_h)

for i in range(50):  # Generate 50 frames
    t = i / 50  
    example_zoom = zoom(t)
    example_zoom.save_frame("zoom_frame_{}.png".format(i)) 
