from sqlalchemy import create_engine
from sqlalchemy import Session

def get_session() -> Session:
    engine = create_engine(
        'postgresql+psycopg2://postgre:23Kuelap!@172.18.0.3:5432/bikedb'
    )