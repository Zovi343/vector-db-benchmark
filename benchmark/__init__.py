import os
from pathlib import Path
import shutil

# Base directory point to the main directory of the project, so all the data
# loaded from files can refer to it as a root directory

BASE_DIRECTORY = Path(__file__).parent.parent
DATASETS_DIR = BASE_DIRECTORY / "datasets"
CODE_DIR = os.path.dirname(__file__)
ROOT_DIR = Path(os.path.dirname(CODE_DIR))
# LVD MODIFICATION START
KUBE_DIR = "/pvc"


def copy_directory(src, dst):
    if not os.path.exists(dst):
        os.makedirs(dst)

    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            copy_directory(s, d)
        else:
            shutil.copy2(s, d)
# LVD MODIFICATION END
