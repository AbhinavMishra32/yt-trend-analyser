import os
import shutil
from scenedetect import open_video, SceneManager, split_video_ffmpeg
from scenedetect.detectors import ContentDetector
from scenedetect.video_splitter import split_video_ffmpeg

def split_video_into_scenes(video_path, threshold=27.0):
    # Open our video, create a scene manager, and add a detector.
    video = open_video(video_path)
    scene_manager = SceneManager()
    scene_manager.add_detector(
        ContentDetector(threshold=threshold))
    scene_manager.detect_scenes(video, show_progress=True)
    scene_list = scene_manager.get_scene_list()
    split_video_ffmpeg(video_path, scene_list, show_progress=True)

def split_music_videos(videos_path, output_path, threshold=40.0):
    """Splits music videos into clips based on scene changes.

    Args:
        videos_path (str): Path to the folder containing music videos.
        output_path (str): Path to the output folder for clips.
        threshold (float, optional): Content detection threshold. Defaults to 30.0.
    """

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    for filename in os.listdir(videos_path):
        if filename.endswith('.mp4'):
            video_path = os.path.join(videos_path, filename)
            
            # Directly use the provided function for scene detection and splitting
            split_video_into_scenes(video_path, threshold) 


def move_clips(current_dir, output_path):
    """Moves generated clip files to the designated output path.

    Args:
        current_dir (str): The directory where the clips were generated.
        output_path (str): The desired output path for the clips. 
    """
    for filename in os.listdir(current_dir):
        if 'Scene' in filename:
            shutil.move(filename, output_path)


if __name__ == "__main__":
    music_videos_folder = "music_videos"
    clips_folder = "clips"
    split_music_videos(music_videos_folder, clips_folder)
    move_clips(os.getcwd(), "clips")
