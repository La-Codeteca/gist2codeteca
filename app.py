from os import getenv
from github_manager import get_gist_id,\
                           publis_gist,\
                           get_tags,\
                           calcule_new_tag,\
                           create_tag,\
                           create_release
from gist_manager import generate_pill
from file_manager import save_gist_in_file
from database_manager import create_table,\
                             get_all_data

owner=getenv("GH_REPO_OWNER")
repo=getenv("GH_REPO")


def main():
    create_table()
    processed_gists = get_all_data()
    gist_id_list = get_gist_id()
    unprocessed_gists = list(set(gist_id_list).difference(set(processed_gists)))
    print(len(unprocessed_gists))
    if(len(unprocessed_gists) == 0):
        print("No hay gist nuevos")
        exit()

    print("Sin procesar:")
    print(unprocessed_gists) 

    save_gist_in_file(unprocessed_gists)
    generate_pill(unprocessed_gists)
    
    #Subir ficheros automaticamente a gitlab
    '''
    sha_commit = publis_gist(unprocessed_gists)

    #Tagear version
    tags = get_tags(owner="La-Codeteca",\
                    repo="la-codeteca.github.io")
    new_tag = calcule_new_tag(tags)
    create_tag(tag=new_tag,\
           sha=sha_commit,\
           owner=owner,\
           repo=repo)
    
    create_release(tag=new_tag,\
           owner=owner,\
           repo=repo)
    '''
    # ToDo: Notificar la subida

main()
