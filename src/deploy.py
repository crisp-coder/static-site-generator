from os.path import abspath, exists, isdir
from os import mkdir
from shutil import rmtree, copytree

def deploy():
    dest=abspath("public")
    if exists(dest) and isdir(dest):
        print(f'Removing dir {dest}')
        rmtree(dest)

    mkdir(dest)

    source=abspath("static")
    if exists(source) and isdir(dest):
        print(f'Copying {source} to {dest}')
        copytree(source, dest, dirs_exist_ok=True)

