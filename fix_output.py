import os
import shutil
from pathlib import Path


# path =cache/raw | rgb/fgawefawjiowfe
# files = list of files in folder
# base name = date + scene (final name)
def fix_path(path, files, base_name, with_json: bool = True):
    type = "rgb" if "rgb" in path else "bands"
    src_folder = Path(path) / Path(files[0]).parent
    final_path = Path("data/raw") / base_name
    os.makedirs(final_path, exist_ok=True)
    if with_json:
        files.append(str(Path(files[0]).parent / "request.json"))

    # print(f"Moving from {src_folder} to {final_path}")
    # print(f"Files: {files}")
    # print(f"Base: {base_name}")
    # fix files name
    for file in files:
        file = Path(file)
        src = Path(path) / file
        new_name = file.with_stem(file.stem + f"_{type}")
        dst = final_path / new_name.name
        # print(dst)
        # os.replace(src,dst)
        shutil.copy(src, dst)

    print(f"Moved from {src_folder} to {final_path}")

# fix_path("cache/raw/rgb/496ceeef5210f23ffff65483049f026c", ["request.json", "response.png"], "2025-07-20")
# fix_path("cache/raw/bands/59c370ae2ae320f2d3ff07ce77477c6a", ["request.json", "response.tiff"], "2025-07-20")
