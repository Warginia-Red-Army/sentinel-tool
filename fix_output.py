import os
import shutil

def fix_path(path, files, base_name):
    for file in files:
        src = os.path.join(path, file)
        dst = f"data/raw/{base_name}/{file}"
        os.makedirs(dst, exist_ok=True)
        os.replace(src,dst)

    print(f"Moved from {path} to {dst}")

