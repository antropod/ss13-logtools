from re import fullmatch
import zipfile
import os
from concurrent.futures import ThreadPoolExecutor
import logging


logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] - %(levelname)s - %(message)s"
)


def test_archive(filename):
    logger.info("Testing %s", filename)
    is_good = True
    with zipfile.ZipFile(filename) as zf:
        if zf.testzip():
            is_good = False
            logger.error("File corrupted: %s", filename)
    if not is_good:
        os.rename(filename, '_' + filename)


def test_archives(directory):
    all_names = [os.path.join(directory, filename) for filename in os.listdir(directory)]
    pool = ThreadPoolExecutor(8)
    pool.map(test_archive, all_names)


def main():
    test_archives("logs")


if __name__ == "__main__":
    main()