import json

def pretty_json(ugly_json):
    json_formatted_str = json.dumps(ugly_json, indent=2)
    return json_formatted_str