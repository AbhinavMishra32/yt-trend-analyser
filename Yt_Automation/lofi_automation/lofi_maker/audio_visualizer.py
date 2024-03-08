import moviepy.editor as mp
import numpy as np

# Function to generate a simple music visualizer
def generate_visualization(audio_path, output_path):
    # Load the audio file
    audio_clip = mp.AudioFileClip(audio_path)

    # Define the function to create a frame for each timestamp
    def make_frame(t):
        # Read a segment of the audio corresponding to time t
        segment = audio_clip.get_frame(t)

        # Calculate the mean intensity of the segment
        intensity = np.mean(segment)

        # Create a black background
        frame = np.zeros((480, 640, 3), dtype=np.uint8)

        # Draw a rectangle with height proportional to the intensity
        height = int(intensity * 200)
        frame[-height:, :, :] = [255, 255, 255]  # White color

        return frame

    # Create the video clip with the defined frame generator
    visual_clip = mp.VideoClip(make_frame, duration=audio_clip.duration)

    # Write the video file to the output path
    visual_clip.write_videofile(output_path, fps=24)

# Example usage
if __name__ == "__main__":
    audio_path = "Mozzy - Seasons (with Sjava & Reason).wav"
    output_path = "output_visualization.mp4"
    generate_visualization(audio_path, output_path)
