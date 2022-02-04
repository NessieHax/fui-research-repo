import os, shutil, sys

def clean(path:str) -> None:
    for root, dirs, files in os.walk(path):
        [shutil.rmtree(os.path.join(root, dir)) for dir in dirs]
        [os.remove(os.path.join(root, file)) for file in files]

def print_err(*values: object, sep: str | None = None, end: str | None = None) -> None:
    print(values, sep=sep, end=end, file=sys.stderr)
    exit(1)