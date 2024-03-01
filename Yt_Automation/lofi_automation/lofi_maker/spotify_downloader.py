import subprocess
import shutil
import os

def download(playlist_url):
    subprocess.run(["spotdl",playlist_url ])

def change_file_types(folder_path, old_extension, new_extension):
    # Iterate through all files in the folder
    for filename in os.listdir(folder_path):
        # Check if the file ends with the old extension
        if filename.endswith(old_extension):
            # Construct the old and new file paths
            old_file_path = os.path.join(folder_path, filename)
            new_file_path = os.path.join(folder_path, filename[:-len(old_extension)] + new_extension)
            # Rename the file
            os.rename(old_file_path, new_file_path)

def move_files(src_folder, dest_folder):
    for filename in os.listdir(src_folder):
        if not filename.startswith(".") and not filename.endswith(".wav"):  # Skip dot files and .wav files
            old_file_path = os.path.join(src_folder, filename)
            new_file_path = os.path.join(dest_folder, filename)
            print(f"Moving {old_file_path} to {new_file_path}")
            shutil.move(old_file_path, new_file_path)
            print(f"File moved successfully!")


if __name__ == "__main__":
    playlist = "https://open.spotify.com/track/51xpNYObJdiEnbvpjoAE8E?si=c4d711c21d3541f8"

    download(playlist) #downloading the lofi playlist from spotify
    songs_folder = "source/songs/normal_songs/" #normal songs folder path
    # change_file_types(".", ".mp3", ".wav")
    # move_files(".", songs_folder)
