
# Imports: from pathlib import Path
def find_files(startpath, recurse=False):
    files_in_startpath = []
    include_list = (".mp3", ".wav", ".m4a")
    for child in Path(startpath).glob("*"):
        if Path(child).is_file and child.suffix in include_list:
            files_in_startpath.append(child)
            if not recurse:
                return files_in_startpath

        elif Path(child).is_dir and recurse:
            files_in_startpath.extend(find_files(child, recurse=True))
    
    return files_in_startpath