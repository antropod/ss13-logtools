import os
from zipfile import ZipFile, BadZipFile
from tqdm import tqdm

import logging


logging.basicConfig(level=logging.INFO, format='[%(asctime)s] - %(levelname)s - %(message)s')
LOG = logging.getLogger(__name__)


def check_archives(directory, delete_bad=False):
    files = os.listdir(directory)
    bad_files = []
    for filename in tqdm(files, desc="Checking archives"):
        try:
            archive_filename = os.path.join(directory, filename)
            with ZipFile(archive_filename):
                pass
        except BadZipFile:
            bad_files.append(archive_filename)
    print(f"{len(bad_files)} bad files found")
    if delete_bad:
        for filename in bad_files:
            os.unlink(filename)


def main():
    check_archives("logs", delete_bad=True)


if __name__ == "__main__":
    main()