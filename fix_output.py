import os
import shutil
from pathlib import Path


# path =cache/raw | rgb/fgawefawjiowfe
# files = list of files in folder
# base name = date + scene (final name)
def fix_path(path, files, base_name):
    type = "rgb" if "rgb" in path else "bands"
    final_path = f"data/raw/{base_name}"
    # fix files name
    for file in files:
        old_name = Path(file)
        src = os.path.join(path, file)
        new_name = old_name.with_stem(old_name.stem + f"_{type}")
        dst = f"{path}/{new_name}"
        print(dst)
        os.replace(src,dst)

    os.makedirs(final_path, exist_ok=True)
    shutil.copy(path, final_path)

    print(f"Moved from {path} to {final_path}")

fix_path("cache/raw/rgb/496ceeef5210f23ffff65483049f026c", ["request.json", "response.png"], "test_date")
