import os
import re
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
        if not new_dir.is_dir():
            shutil.copytree(template_dir, new_dir)
            print(f"Template directory copied to {new_dir}")
        else:
            print("file already exists")
    except Exception as e:
        print(f"An error occurred while copying the template directory: {e}")
        exit(1)

    return new_dir


def find_file_with_regex(directory, pattern):
    regex = re.compile(pattern)
    for file_name in os.listdir(directory):
        if regex.match(file_name):
            return directory / file_name
    return None


def move_file(file_to_move, destination):
    try:
        if file_to_move.is_file() or file_to_move.is_dir():
            shutil.move(file_to_move, destination)
            print(f"{file_to_move.name} moved to {destination}")
        else:
            raise FileNotFoundError(f"File not found! '{file_to_move}'")
    except Exception as e:
        print(f"An error occurred while moving the file: {e}")


def find_largest_run_number(directory) -> int:
    largest_number = 0
    pattern = re.compile(r"run(\d+)")

    for dir_name in os.listdir(directory):
        match = pattern.match(dir_name)
        if match:
            num = int(match.group(1))
            if num > largest_number:
                largest_number = num

    return largest_number


def move_files_to_new_dir(logs_dir, new_dir):
    directory = logs_dir / 'output'
    parse_directory = logs_dir / 'output' / 'parse'

    file_to_move = logs_dir / 'log'

    mlc_destination = new_dir / 'snc3' / 'linux' / 'mlc'
    hpl_destination = new_dir / 'snc3' / 'linux' / 'hpl'
    spec_cpu_sir_destination = new_dir / 'snc3' / 'linux' / 'spec2017-1.0.2-GCC8.1-O2' / 'sir'
    spec_cpu_sfp_destination = new_dir / 'snc3' / 'linux' / 'spec2017-1.0.2-GCC8.1-O2' / 'sfp'
    stream_destination = new_dir / 'snc3' / 'linux' / 'stream'
    miscellaneous_destination = new_dir / 'snc3' / 'linux' / 'miscellaneous'


    run_number = 1 + find_largest_run_number(mlc_destination)

    print(f"Current run is: {run_number}")

    mlc_destination = mlc_destination / f"run{run_number}"
    hpl_destination = hpl_destination / f"run{run_number}"
    spec_cpu_sir_destination = spec_cpu_sir_destination / f"run{run_number}"
    spec_cpu_sfp_destination = spec_cpu_sfp_destination / f"run{run_number}"
    stream_destination = stream_destination / f"run{run_number}"
    miscellaneous_destination = miscellaneous_destination / f"run{run_number}"

    mlc_destination = Path(mlc_destination)
    mlc_destination.mkdir(parents=True, exist_ok=True)

    hpl_destination = Path(hpl_destination)
    hpl_destination.mkdir(parents=True, exist_ok=True)

    spec_cpu_sir_destination = Path(spec_cpu_sir_destination)
    spec_cpu_sir_destination.mkdir(parents=True, exist_ok=True)

    spec_cpu_sfp_destination = Path(spec_cpu_sfp_destination)
    spec_cpu_sfp_destination.mkdir(parents=True, exist_ok=True)

    stream_destination = Path(stream_destination)
    stream_destination.mkdir(parents=True, exist_ok=True)

    miscellaneous_destination = Path(miscellaneous_destination)
    miscellaneous_destination.parent.mkdir(parents=True, exist_ok=True)
    miscellaneous_destination.mkdir(parents=True, exist_ok=True)

    if file_to_move:
        destination = str(new_dir / file_to_move.name)
        move_file(file_to_move, destination)


    pattern = r"mlc.csv"
    file_to_move = find_file_with_regex(directory, pattern)
    if file_to_move:
        destination = mlc_destination / file_to_move.name
        move_file(file_to_move, destination)


    pattern = r"mlc_\d{4}-\d{2}-\d{2}_\d{2}\.\d{2}\.\d{2}\.log"
    file_to_move = find_file_with_regex(directory, pattern)
    if file_to_move:
        destination = mlc_destination / file_to_move.name
        move_file(file_to_move, destination)


    pattern = r"linpack_\d{4}-\d{2}-\d{2}_\d{2}\.\d{2}\.\d{2}\.log"
    file_to_move = find_file_with_regex(directory, pattern)
    if file_to_move:
            destination = hpl_destination / file_to_move.name
            move_file(file_to_move, destination)

    pattern = r"linpack.csv"
    file_to_move = find_file_with_regex(directory, pattern)
    if file_to_move:
            destination = hpl_destination / file_to_move.name
            move_file(file_to_move, destination)

    pattern = r"linpack.csv"
    file_to_move = find_file_with_regex(parse_directory, pattern)
    if file_to_move:
            destination = hpl_destination / 'parse' / file_to_move.name
            destination = Path(destination)
            destination.parent.mkdir(parents=True, exist_ok=True)
            move_file(file_to_move, destination)

    pattern = r"cpu2017-\d{1}.\d{1}.\d{1}_intrate.zip"
    file_to_move = find_file_with_regex(directory, pattern)
    if file_to_move:
            destination = spec_cpu_sir_destination / file_to_move.name
            move_file(file_to_move, destination)

    pattern = r"cpu2017-\d{1}.\d{1}.\d{1}_fprate.zip"
    file_to_move = find_file_with_regex(directory, pattern)
    if file_to_move:
            destination = spec_cpu_sir_destination / file_to_move.name
            move_file(file_to_move, destination)

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

    move_files_to_new_dir(logs_dir, new_dir)
    print("Logs moved successfully!")


