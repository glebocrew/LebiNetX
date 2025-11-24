from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import List

from PASSWORDS import HOST, PORT, USER, PASSWORD, DATABASE
from mariadb.db_models import User

engine = create_engine(f"mariadb+mariadbconnector://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")
sessionmaker_local = sessionmaker(
    autoflush=False,
    autocommit=True, 
    bind=engine
)

class DataBase:
    def get_users() -> List[User]:
        