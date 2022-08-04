from sqlalchemy import create_engine


def create_default_engine():
    return create_engine("sqlite:///logs.db")