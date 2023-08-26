import yaml
import requests 

def get_parameter(file_path):
    r = requests.get(file_path)
    parameter = yaml.safe_load(r.content)

    return parameter

