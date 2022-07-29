from logtools.parsers.uplink import UplinkTxtParser


def main():
    for record in UplinkTxtParser().parse_file_from_archive("logs_2022", "round-187217.zip"):
        print(record)


if __name__ == "__main__":
    main()