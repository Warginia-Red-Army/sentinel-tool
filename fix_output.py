import os
import shutil
from pathlib import Path

def fix_path(path, files, base_name, with_json: bool = True, suffix: str = ""):
    src_folder = Path(path) / Path(files[0]).parent
    final_path = Path("data/raw") / base_name
    os.makedirs(final_path, exist_ok=True)
    if with_json:
        files.append(str(Path(files[0]).parent / "request.json"))
    for file in files:
        file = Path(file)
        src = Path(path) / file
        new_name = file.with_stem(file.stem + f"_{suffix}")
        dst = final_path / new_name.name
        # print(dst)
        # os.replace(src,dst)
        shutil.copy(src, dst)

    print(f"Moved from {src_folder} to {final_path}")