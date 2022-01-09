import os, shutil

def clean(path:str) -> None:
    for root, dirs, files in os.walk(path):
        [shutil.rmtree(os.path.join(root, dir)) for dir in dirs]
        [os.remove(os.path.join(root, file)) for file in files]