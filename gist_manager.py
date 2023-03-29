import glob, os, json
from jinja2 import Environment, FileSystemLoader, select_autoescape
import pathlib
from database_manager import insert_data

#os.chdir("./gists")


def extension2type(extension:str):
    if extension == ".py":
        return "python"
    elif extension == ".sh":
        return "bash"
    elif extension == ".js":
        return "javascript"
    elif extension == ".jsx":
        return "react"
    elif extension == ".md":
        return "apuntes"
    return ""


def create_title(name:str):
    return name.replace("_", " ")

def generate_markdown_document(id:str, name:str, tag:str, description: str, embebed:str):
        env = Environment(
        loader=FileSystemLoader("/code"),
        autoescape=select_autoescape()
        )


        t = env.get_template("template.md")

        render = t.render(title=name, tag=tag, description=description, content=embebed)
        with open(f"/code/pills/{id.lower()}.md","w") as f:
            f.write(render)

def generate_pill(files):
    #for file in glob.glob("*.json"):
    for file in files:
        print(f"Abriendo: {file}")

        f = open(f"/code/gists/{file}.json")
        data = json.load(f)    
        f.close()
        
        id = data['id']
        description = data['description']
        embebed = f'<script src="https://gist.github.com/crakernano/{id}.js"></script>'
        files = data['files']

        print(f"ID: {id}")
        print(f"Descripcion: {description}")
        print(f"Contenido: {embebed}")

        for file in files:
            file_extension = pathlib.Path(file).suffix
            name = pathlib.Path(file).stem
            name = create_title(name)
            type = extension2type(file_extension)
            print(f"Tipo: {file_extension}({type})")
            print(f"Nombre: {name}")

        print("#" * 20)

        generate_markdown_document(id=id,\
                                    name=name,\
                                    tag=type,\
                                    description=description,\
                                    embebed=embebed)
        
        insert_data(data=id)
        

