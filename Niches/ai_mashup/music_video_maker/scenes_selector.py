import os
import re

clip_number = 2
scenes_number = [15, 21, 4]

scenes = os.listdir('clips')

for scene in scenes:
    match = re.match(r'(\d+)-Scene-(\d+)\.mp4', scene)
    if match:
        clip_num, scene_num = map(int, match.groups())
        if clip_num == clip_number and scene_num not in scenes_number:
            os.remove('clips/' + scene)
