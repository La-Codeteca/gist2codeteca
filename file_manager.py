import json
from github_manager import get_gist

def save_gist_in_file(gist_list):
    for gist in gist_list:
        g = get_gist(gist)
        FILENAME = f"{gist}.json"
        with open(f"/code/gists/{FILENAME}", 'w', encoding='utf-8') as f:
            json.dump(g, f, ensure_ascii=False, indent=4)