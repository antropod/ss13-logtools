import pandas as pd
from sqlalchemy import create_engine


def read_file(filename):
    with open(filename) as fp:
        return fp.read()

def main():
    engine = create_engine("sqlite:///logs.db")
    sql_query = read_file("sql/jobs.sql")
    with engine.connect() as conn:
        df = pd.read_sql(sql_query, conn, parse_dates="dt")
    df.to_excel("raw_data.xlsx", index=False)
    # pivot = df.pivot_table(index="dt", columns="assigned_role", values="hits")
    # pivot.to_excel("jobs.xlsx", index=False)

    # print(pivot.head())


if __name__ == "__main__":
    main()