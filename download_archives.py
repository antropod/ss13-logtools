import argparse
import json
import os
import os.path
import urllib.request
import logging
import requests
import socket
import time

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

    for entry in file_list:
        url = entry["url"]
        filename = os.path.join(args.directory, entry["name"])
        if os.path.exists(filename):
            logger.info("%s already exists", filename)
            continue
        try:
            download(url, filename)
        except Exception as e:
            logger.exception("Failed to download %s", url)
        # time.sleep(5)


if __name__ == "__main__":
    main()