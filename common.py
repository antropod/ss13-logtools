from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def create_default_engine():
    return create_engine("sqlite:///logs.sqlite")


engine = create_default_engine()
Session = sessionmaker(bind=engine)