from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from typing import List, Optional, Dict

from _db.PASSWORDS import HOST, PORT, USER, PASSWORD, DATABASE
from _db.db_models import User

from logger import Logger

logger = Logger("logs/db_logs.txt")


class DataBase:
    def __init__(self):
        self.engine = create_engine(
            f"mysql+mysqlconnector://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
        )

        self.sessionmaker_local = sessionmaker(
            autoflush=False, autocommit=False, bind=self.engine
        )

    def get_users(self) -> Optional[List[User]]:
        """
        Getting all users

        :return: List of Database User model
        :rtype: List[User]
        """
        logger.log("l", "Getting all users...")
        try:
            with self.sessionmaker_local.begin() as session:
                statement = select(User)
                users = session.execute(statement)
                users_result = users.scalars()
                users = []
                for user in users_result:
                    print(user.userId)
                    users.append(
                        {
                            "userId": user.userId,
                            "nickname": user.nickname,
                            "email": user.email,
                            "createdAt": user.createdAt,
                            "updatedAt": user.updatedAt,
                            "avatar": user.avatar,
                        }
                    )
                if users == []:
                    return None
                return users
        except Exception as e:
            logger.log(
                "e",
                f"The operation of getting all users was incomplete! Full exception {e}",
            )

    def get_user(
        self,
        userId: Optional[str] = None,
        email: Optional[str] = None,
        nickname: Optional[str] = None,
    ) -> Optional[Dict]:
        """
        Gets one user

        :return: List of Database User model
        :rtype: List[User]
        """
        if userId is None and email is None and nickname is None:
            logger.log(
                "e",
                "At least of argument should be not None while calling `get_user`. Please, select userId/email/nickname",
            )
            return None

        logger.log("l", "Getting all users...")

        conditions = []
        if userId is not None:
            conditions.append(User.userId == userId)
        if email is not None:
            conditions.append(User.email == email)
        if nickname is not None:
            conditions.append(User.nickname == nickname)

        print(f"NICKNAME: {nickname}")

        try:
            with self.sessionmaker_local.begin() as session:
                statement = select(User).where(*conditions)
                print(statement)
                user = session.execute(statement).scalar()

                return {
                    "userId": user.userId,
                    "nickname": user.nickname,
                    "email": user.email,
                    "createdAt": user.createdAt,
                    "updatedAt": user.updatedAt,
                    "avatar": user.avatar,
                }

        except Exception as e:
            logger.log(
                "e", f"The operation of getting user was incomplete! Full exception {e}"
            )
