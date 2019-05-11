def traverse(dirs):
    for root, dirs, files in os.walk(dirs):
        for file in files:
            if file.endswith(".txt"):
                print(os.path.join(root, file))

def get_files(work_dir: object) -> object:
    file_list = os.scandir(work_dir)
    for the_file in file_list:
        print(the_file)
