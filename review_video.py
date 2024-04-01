import subprocess
import os

def run_command_in_directory(command, directory):
    # Change directory to the specified directory
    os.chdir(directory)

    # Run the command in the specified directory
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()

    # Decode the output
    output = output.decode('utf-8')
    error = error.decode('utf-8')

    # Print the output and error
    print("Output:", output)
    if error:
        print("Error:", error)

# Example usage
if __name__ == "__main__":
    directory_path = "/path/to/your/directory"
    command_to_run = "ls -l"
    run_command_in_directory(command_to_run, directory_path)
