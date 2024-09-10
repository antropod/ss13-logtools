import os
import pandas as pd
from sqlalchemy import create_engine

from common import create_default_engine
from logtools.util import read_file
from openpyxl import Workbook

engine = create_default_engine()


SQL_DIR = "sql"
REPORTS_DIR = "reports"


def make_reports():
    if not os.path.exists(REPORTS_DIR):
        os.mkdir(REPORTS_DIR)

    query = read_file(os.path.join(SQL_DIR, "metrics_detail.sql"))
    print(query)
    with engine.connect() as conn:
        df_curr = pd.read_sql(query, conn, parse_dates="dt")

    engine_prev = create_engine("sqlite:///logs.bak.sqlite")
    with engine_prev.connect() as conn:
        df_prev = pd.read_sql(query, conn, parse_dates="dt")

    df_curr.to_excel(os.path.join(REPORTS_DIR, "metrics_curr.xlsx"))
    df_prev.to_excel(os.path.join(REPORTS_DIR, "metrics_prev.xlsx"))

def main():
    make_reports()


if __name__ == "__main__":
    main()