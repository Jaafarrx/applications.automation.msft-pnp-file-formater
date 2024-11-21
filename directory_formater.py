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


def directory_formater(logs_dir, remote_server) -> bool:
    result = False
    largest_number = find_largest_number(remote_server)

    if largest_number == -1:
        print("Failed to find largest file number")
        return result
    else:
        print(f"Largest file found: {largest_number}")

    new_file_number = largest_number + 1
    template_dir = Path(fr"{remote_server}\_template_ryne_latest")

    try:
        if template_dir.is_dir():
            print("template dir found!")
            print(f"template dir: {template_dir}")
        else:
            raise FileNotFoundError(f"Template directory '{template_dir}' not found!")
    except Exception as e:
        print(f"An error occurred: {e}")
        exit(1)


    return result


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

    result = directory_formater(logs_dir, remote_server)
    if result:
        print("Conversion Succeeded!")
    else:
        print("Conversion Failed!")
