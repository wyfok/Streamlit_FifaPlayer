import yaml

def get_parameter(file_path):
    with open(file_path, 'r') as file:
        parameter = yaml.safe_load(file)

    return parameter

