from page_builder import generate_page
from shutil import rmtree, copytree
from os.path import abspath, exists, isdir, join, isfile, relpath
from os import listdir, mkdir
from sys import argv

def get_file_paths(directory, files):
    # Build a list of files in the content
    # directory and subdirectories
    # Output is saved in files parameter
    if exists(directory):
        for entry in listdir(directory):
            full_path = join(directory, entry)
            if isfile(full_path):
                files.append(full_path)
            elif isdir(full_path):
                get_file_paths(full_path, files)

def main():
    # Base path is a string to use when hosting the site on github pages.
    base_path = '/'
    if len(argv) == 2:
        base_path = argv[1]
    print(f'base_path is {base_path}')

    # public_dir is the directory to store the generated site.
    public_dir = "docs"
    # content dir is the directory the markdown files are stored.
    content_dir = "content"
    # static dir is the directory the static assets files are stored.
    static_dir = "static"

    # Delete and remake public directory
    if isdir(abspath(public_dir)):
        rmtree(abspath(public_dir))
    mkdir(abspath(public_dir))

    content_files=[]
    get_file_paths(content_dir, content_files)

    for file in content_files:
        print(f'{file}')
        dest_path = abspath(public_dir)
        print(f'dest_path = {dest_path}')
        generate_page(
            file,
            "template.html",
            dest_path,
            base_path,
            content_dir
        )

    # Copy the static assets to the public folder.
    if exists(abspath(static_dir)):
        public_base_path = abspath(public_dir)
        copytree(static_dir, public_base_path, dirs_exist_ok=True)

if __name__ == "__main__":
    main()
