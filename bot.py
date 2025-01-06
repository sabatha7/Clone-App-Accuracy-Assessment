import os
import time
import subprocess

def sniff_directory(directory):
    """
    Monitors a specified directory for new files, processes the first file found,
    and writes the output to a text file in the "notify-groups-task" directory.

    Args:
        directory (str): The path to the directory to be monitored.

    The function performs the following steps in an infinite loop:
    1. Lists all files in the specified directory.
    2. If files are found, processes the first file by running a Python script (app.py) with the file as an argument.
    3. Captures the output of the script and writes it to a text file in the "notify-groups-task" directory.
    4. Deletes all files in the monitored directory.
    5. Waits for 10 seconds before repeating the process.
    """
    while True:
        files = os.listdir(directory)
        if files:
            first_file = os.path.join(directory, files[0])
            file_name_without_extension = os.path.splitext(first_file)[0]
            output_file = os.path.join("notify-groups-task", f"{os.path.basename(file_name_without_extension)}.txt")
            with open(output_file, 'w') as f:
                result = subprocess.run(["python", "app.py", first_file], capture_output=True, text=True).stdout
                f.write(result)
            for file in os.listdir(directory):
                os.remove(os.path.join(directory, file))
        time.sleep(10)

if __name__ == "__main__":
    directory_to_sniff = "groups-task"
    sniff_directory(directory_to_sniff)