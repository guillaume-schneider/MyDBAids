import os


def set_to_dict(value: set) -> list:
    my_dict = {}
    for key, value in value.items():
        my_dict[key] = list(value) if value else []
    return my_dict

def get_json_files_in_dir(directory):
    json_files = [f for f in os.listdir(directory) if f.endswith('.json')]
    return json_files
