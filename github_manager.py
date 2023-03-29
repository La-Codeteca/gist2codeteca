import requests, base64
from os import getenv
from helpers import pretty_json

BASE_URL = "https://api.github.com"
TOKEN=getenv("GH_TOKEN")
headers = {"Authorization": f"Bearer {TOKEN}",
           "Accept":"application/vnd.github+json", 
           "X-GitHub-Api-Version":"2022-11-28"}


def get_gist(gist_id):
    endpoint = "gists"
    url = f"{BASE_URL}/{endpoint}/{gist_id}"
    print(f"Descargar: {url}")
    response = requests.get(url)

    if(response.status_code != 200):
        print(f"ERROR [{response.status_code}] : {response.text}")
        exit()
    return response.json()

def get_gist_id(username='crakernano'):
    endpoint = f"users/{username}/gists"
    url = f"{BASE_URL}/{endpoint}"
    response = requests.get(url)
    
    if(response.status_code != 200):
        print(f"ERROR [{response.status_code}] : {response.text}")
        exit()
    
    response_json = response.json()
    gist_ids = []

    for gits in response_json: 
        gist_ids.append(gits["id"])
        print(pretty_json(gits["id"]))

    return gist_ids

def push_to_github(file_name:str, owner:str, repo:str):    
    endpoint = f"repos/{owner}/{repo}/contents"
    url = f"{BASE_URL}/{endpoint}/{file_name}.md"
    gist_path = f"/code/pills/{file_name}.md"

    print(f"Atacando: {url}")
    
    with open(gist_path, "rb") as f:        
        encodedData = base64.b64encode(f.read())

        headers = {
            "Authorization": f"Bearer {TOKEN}",
            "Content-type": "application/vnd.github+json"
        }

        data = {
            "message": f"Add: {file_name}", 
            "content": encodedData.decode("utf-8")
        }

        r = requests.put(url, headers=headers, json=data)
        print(f"[{r.status_code}] {r.text}") 
        
def publis_gist(gists:list):
    for gist in gists:
        print(f"Subiendo a github: {gist}")        
        push_to_github(gist,\
                       owner=getenv("GH_REPO_OWNER"),\
                       repo=getenv("GH_REPO"))


def get_tags(owner:str, repo:str):
    endpoint = f"repos/{owner}/{repo}/tags"
    url = f"{BASE_URL}/{endpoint}"
    print(f"Atacando: {url}")

    r = requests.get(url, headers=headers)
    tags = r.json()
    tag_list = []
    for tag in tags:        
        tag_list.append(tag["name"])
    
    return tag_list

def calcule_new_tag(tags:list):
    last_tag = tags[0]
    print( f"Version publicada: {last_tag}" )

    tag = last_tag.split(".")    
    revision = int(tag[1]) + 1
    print( f"Proxima versión: {tag[0]}.{revision}.{tag[2]}" )
    return f"{tag[0]}.{revision}.{tag[2]}"

def create_tag(tag:str,\
               sha:str,\
               owner:str,\
               repo:str,\
               branch = "master",\
               msg = "update content"):
    
    url = f"{BASE_URL}/repos/{owner}/{repo}/git/tags"

    data = {
        "tag":tag,
        "message": msg,
        "object":sha,
        "type":"commit",
        }
    
    r = requests.post(url, headers=headers, json=data)
    print(f"[{r.status_code}] {r.text}") 

def create_release(tag:str,\
                   owner:str,\
                   repo:str,\
                   branch = "master",\
                   msg = "Automatic update content"):    

    url = f"{BASE_URL}/repos/{owner}/{repo}/releases"

    data = {
        "tag_name":tag,
        "target_commitish":branch,
        "name":tag,
        "body":msg,
        "draft":False,
        "prerelease":False,
        "generate_release_notes":False}
    
    r = requests.post(url, headers=headers, json=data)
    print(f"[{r.status_code}] {r.text}") 