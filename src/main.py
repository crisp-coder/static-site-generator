from page_builder import generate_page
from shutil import rmtree, copytree
from os.path import abspath, exists, isdir, join, isfile, relpath
from os import listdir, mkdir

def get_file_paths(directory, files):
    if exists(directory):
        for entry in listdir(directory):
            full_path = join(directory, entry)
            if isfile(full_path):
                files.append(full_path)
            elif isdir(full_path):
                get_file_paths(full_path, files)
def main():
    public_dir = "public"
    content_dir = "content"
    if isdir(abspath(public_dir)):
        rmtree(abspath(public_dir))
    mkdir(abspath(public_dir))

    content_files=[]
    get_file_paths(content_dir, content_files)

    for file in content_files:
        print(f'{file}')
        pruned_file = file[len(content_dir)+1:-2]
        pruned_file += 'html'
        generate_page(file, "template.html", abspath(join(abspath(public_dir), pruned_file)))

    static_dir = "static"
    if exists(abspath(static_dir)):
        print(f'Copying {static_dir} to {public_dir}')
        copytree(static_dir, abspath(public_dir), dirs_exist_ok=True)

if __name__ == "__main__":
    main()
