from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from typing import List

from mariadb.PASSWORDS import HOST, PORT, USER, PASSWORD, DATABASE
from mariadb.db_models import User




class DataBase:
    def __init__(self):
        self.engine = create_engine(
        f"mysql+mysqlconnector://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
        )

        self.sessionmaker_local = sessionmaker(autoflush=False, autocommit=False, bind=self.engine)
    
    def get_users(self) -> List[User]:
        with self.sessionmaker_local.begin() as session:
            statement = select(User)
            users = session.execute(statement)
            users_result = users.scalars()

            if users_result != []:
                users = []
                for user in users_result:
                    print(user.userId)
                    users.append({
                        "userId": user.userId,
                        "nickname": user.nickname, 
                        "email": user.email,
                        "createdAt": user.createdAt,
                        "updatedAt": user.updatedAt,
                        "avatar": user.avatar
                    })
                return users
            else:
                return -1
