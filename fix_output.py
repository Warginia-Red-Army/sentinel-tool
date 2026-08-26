import os
import shutil


# path =cache/raw | rgb/fgawefawjiowfe
# files = list of files in folder
# base name = date + scene (final name)
def fix_path(path, files, base_name):
    type = "rgb" if "rgb" in path else "bands"
    final_path = f"data/{base_name}"
    # fix files name
    for file in files:
        src = os.path.join(path, file)
        dst = f"{path}/{file}_{type}"
        os.replace(src,dst)

    shutil.copy(path, final_path)

    print(f"Moved from {path} to {dst}")

fix_path("cache/raw/rgb/496ceeef5210f23ffff65483049f026c", ["request.json", "response.png"], "test_date")
