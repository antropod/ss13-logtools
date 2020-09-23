from zipfile import ZipFile
import re
from collections import namedtuple
import pandas as pd
import sys

ROUNDS_ARCHIVE = 'data/month.2020-09.zip'
OUTPUT_FILENAME = 'manuel-2020-09-cargo.xlsx'


def log_error(*args, **kwargs):
    kwargs['file'] = sys.stderr
    print(*args, **kwargs)


def parse_round_id(filename):
    m = re.search(r"round-(\d+)", filename)
    return int(m.group(1))


def iterdata(filename):
    with ZipFile(filename, 'r') as zf:
        for zi in zf.infolist():
            if zi.filename.endswith('cargo.html'):
                round_id = parse_round_id(zi.filename)
                yield round_id, zf.read(zi.filename).decode('utf-8')
    

def match_order(log_line):
    """
    >>> match_order("05:35:25 [0x2032bcd] (152,108,1) || the supply shuttle Order #447 (Janitorial Supplies Crate, placed by test/(Test Tester)), paid by Cargo Budget has shipped.")
    ('447', 'Janitorial Supplies Crate', 'test', 'Test Tester', 'Cargo Budget')
    """
    m = re.search(r"Order #(\d+) \((.+), placed by (.+)/\((.+)\)\), paid by (.+) has shipped.", log_line)
    shipment_order = 'has shipped' in log_line
    if bool(m) != bool(shipment_order):
        log_error("Failed to parse cargo order, check your regex: {}".format(log_line))
    if m:
        return m.groups()
    return None


CargoShippedOrders = namedtuple('CargoShippedOrders', ['round_id', 'order_id', 'pack_name', 'ckey', 'ic_name', 'account_holder'])


def list_packs(it):
    for round_id, cargo_html in it:
        lines = [x.strip('\r\n') for x in cargo_html.split('<br>')]
        for line in lines:
            m = match_order(line)
            if m:
                yield CargoShippedOrders(round_id, *m)

                
def main():
    data_txt = iterdata(ROUNDS_ARCHIVE)
    packs = list_packs(data_txt)

    df = pd.DataFrame(packs)
    df.to_excel(OUTPUT_FILENAME, index=False)
    
    
if __name__ == '__main__':
    main()