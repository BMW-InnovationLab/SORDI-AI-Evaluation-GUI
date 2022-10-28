import json

def parse_json(file_path:str) -> object:
    with open(file_path, "rb") as json_file:
        return json.load(json_file)


def write_json(file_path:str, content:object) -> None:
    with open(file_path, "w") as json_file:
        json_file.write(json.dumps(content))


def jsonify_string(content:str) -> object:
    return json.loads(content)