import os
import shutil
from pathlib import Path


def find_largest_number(remote_server) -> int:
    largest_number = -1

    for file_name in os.listdir(remote_server):
        try:
            file_number = int(file_name)

            if file_number > largest_number:
                largest_number = file_number
        except ValueError:
            continue

    return largest_number


def create_new_results_directory(remote_server) -> Path:
    try:
        largest_number = find_largest_number(remote_server)

        if largest_number == -1:
            raise FileNotFoundError(f"Failed to find largest file number")
        else:
            print(f"Largest file found: {largest_number}")
    except Exception as e:
        print(f"{e}")
        exit(1)

    new_file_number = largest_number + 1
    template_dir = Path(fr"{remote_server}\_template_ryne_latest")

    try:
        if template_dir.is_dir():
            print(f"template dir: {template_dir}")
        else:
            raise FileNotFoundError(f"Template directory '{template_dir}' not found!")
    except Exception as e:
        print(f"An error occurred: {e}")
        exit(1)

    new_dir = Path(f"{new_file_number}")
    try:
        shutil.copytree(template_dir, new_dir)
        print(f"Template directory copied to {new_dir}")
    except Exception as e:
        print(f"An error occurred while copying the template directory: {e}")
        exit(1)

    return new_dir


if __name__  == "__main__":
    remote_server = r"\\10.54.112.76\e\MSFT"
    logs_dir = Path('logs')
    try:
        if logs_dir.is_dir():
            print("Logs dir found!")
        else:
            raise FileNotFoundError(f"Logs directory '{logs_dir}' not found!")
    except Exception as e:
        print(f"An error occurred: {e}")
        print("make sure to add the logs directory to the same dir as this code.")
        exit(1)

    new_dir = create_new_results_directory(remote_server)

