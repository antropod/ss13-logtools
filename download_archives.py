import argparse
import json
import os
import os.path
import urllib.request
import logging
import requests
import socket
import time
from concurrent.futures import ThreadPoolExecutor

socket.setdefaulttimeout(10)


logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] - %(levelname)s - %(message)s"
)


def load_json(filename):
    with open(filename, encoding="utf-8") as fp:
        return json.load(fp)


def _download(url, filename):
    logger.info("Downloading %s to %s", url, filename)
    response = requests.get(url, timeout=10, stream=True)
    with open(filename, 'wb') as fp:
        for chunk in response.iter_content(1024**2):
            fp.write(chunk)


def download(url, filename):
    logger.info("Downloading %s to %s", url, filename)
    urllib.request.urlretrieve(url, filename)


def worker_download(item, directory="logs"):
    url = item["url"]
    filename = os.path.join(directory, item["name"])

    if os.path.exists(filename):
        logger.info("%s already exists", filename)
        return

    try:
        download(url, filename)
    except Exception as e:
        logger.exception("Failed to download %s", url)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    parser.add_argument("-d", "--directory", default="logs")
    return parser.parse_args()


def main():
    args = parse_args()

    file_list = load_json(args.filename)

    if not os.path.exists(args.directory):
        os.mkdir(args.directory)

    pool = ThreadPoolExecutor(8)
    pool.map(worker_download, file_list)


if __name__ == "__main__":
    main()