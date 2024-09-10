import os
import pandas as pd
from sqlalchemy import create_engine

from common import create_default_engine
from logtools.util import read_file
from openpyxl import Workbook

engine = create_default_engine()


SQL_DIR = "sql"
REPORTS_DIR = "reports"


def make_report(name, report_name, *report_names):
    print(f"Making report {name}")
    excel_filename = os.path.join(REPORTS_DIR, name + ".xlsx")
    report_names = (report_name,) + report_names

    with engine.connect() as conn:
        df_list = []
        for report_name in report_names:
            sql_filename = os.path.join(SQL_DIR, report_name + '.sql')
            query = read_file(sql_filename)
            df = pd.read_sql(query, conn, parse_dates="dt")
            df_list.append(df)


    with pd.ExcelWriter(excel_filename) as writer:
        for df, report_name in zip(df_list, report_names):
            df.to_excel(writer, sheet_name=report_name, index=False)


def make_reports():
    if not os.path.exists(REPORTS_DIR):
        os.mkdir(REPORTS_DIR)

    make_report("antag_rates", "antag_rates")
    make_report("saylog", "saylog")
    make_report("russian", "russian")
    make_report("map_pivot", "map_pivot")
    make_report(
        "uplink",
        "uplink_items",
        "uplink_nukeops",
        "changeling_powers",
        "wizard_spell",
        "malf_powers",
        "heretic_knowledge",
    )
    make_report("cargo_orders", "cargo_orders")
    make_report("unique_players", "unique_players")
    make_report("dynamic", "dynamic")
    make_report("dynamic_100", "dynamic_100")


def main():
    make_reports()


if __name__ == "__main__":
    main()