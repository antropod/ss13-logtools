from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from logtools.models.uplink import Uplink



def main():
    engine = create_engine("sqlite:///logs.sqlite")
    Session = sessionmaker(bind=engine)
    with Session.begin() as session:
        query = session.query(Uplink).filter_by(round_id=187250).delete()
        print(query)


if __name__ == "__main__":
    main()