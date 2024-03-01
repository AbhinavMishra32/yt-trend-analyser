import subprocess
import shutil
import os

def download_lofi_playlist(playlist_url):
    subprocess.run(["spotdl",playlist_url, "--print-errors",  ])

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



if __name__ == "__main__":
    playlist = "https://open.spotify.com/album/18NOKLkZETa4sWwLMIm0UZ?si=yc70wdxWRj-7VZLXDNJWSg"

    download_lofi_playlist(playlist) #downloading the lofi playlist from spotify
    songs_folder = "source/songs/normal_songs/" #normal songs folder path
    change_file_types("/", ".mp3", ".wav")
    # shutil.move("lofi_playlist", songs_folder) #moving the downloaded playlist to the normal songs folder