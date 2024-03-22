import pandas as pd
from sqlalchemy import create_engine


def read_file(filename):
    with open(filename) as fp:
        return fp.read()


def main():
    engine = create_engine("sqlite:///logs.sqlite")
    sql_query = read_file("sql/antag_rates.sql")
    with engine.connect() as conn:
        df = pd.read_sql(sql_query, conn, parse_dates="dt")
    df.to_excel("raw_data.xlsx", index=False)


if __name__ == "__main__":
    main()