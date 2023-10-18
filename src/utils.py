import json
import yaml

def read_json(file_path):
    with open(file_path) as f:
        data = json.load(f)
    return data

import yaml

def load_yaml_file(file_path):
    try:
        with open(file_path, 'r') as file:
            data = yaml.safe_load(file)
        return data
    except Exception as e:
        print(f"Error loading YAML file '{file_path}': {e}")
        return None
