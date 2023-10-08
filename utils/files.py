import os


def get_subdirectories(dir_path):
    items = os.listdir(dir_path)
    directories = [dir_path / item for item in items if os.path.isdir(os.path.join(dir_path / item))]
    return directories


def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()
