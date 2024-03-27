import os
import pandas as pd
from sqlalchemy import create_engine

from common import create_default_engine
from logtools.util import read_file
from openpyxl import Workbook


SQL_DIR = "sql"
REPORTS_DIR = "reports"
STATS = [
    ("antag_rates.sql", "antag_rates.xlsx"),
    ("saylog.sql", "saylog.xlsx"),
]


def make_reports():
    if not os.path.exists(REPORTS_DIR):
        os.mkdir(REPORTS_DIR)

    engine = create_default_engine()
    for sql_filename, excel_filename in STATS:
        sql_filename = os.path.join(SQL_DIR, sql_filename)
        excel_filename = os.path.join(REPORTS_DIR, excel_filename)
        print(f"Processing {sql_filename} -> {excel_filename}")
        sql_query = read_file(sql_filename)
        with engine.connect() as conn:
            df = pd.read_sql(sql_query, conn, parse_dates="dt")
        df.to_excel(excel_filename, index=False)
        # with pd.ExcelWriter(excel_filename, mode="w") as excel_writer:
        #     ws = excel_writer.book.create_sheet("Sheet1")
        #     # ws.append([description])
        #     #excel_writer.workbook.worksheets[0].append("Hello world")
        #     df.to_excel(excel_writer, index=False, startrow=0)


def main():
    make_reports()


if __name__ == "__main__":
    main()