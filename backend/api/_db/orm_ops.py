from sqlalchemy import create_engine, select, delete, insert
from sqlalchemy.orm import sessionmaker
from typing import List, Optional, Dict, Tuple
from consts import DEFAULT_AVATAR

from fastapi import status

from _db.PASSWORDS import HOST, PORT, USER, PASSWORD, DATABASE
from _db.db_models import User

from logger import Logger
from uuid import uuid4
from datetime import datetime

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

        :return: List of User jsons
        :rtype: List[dict]
        """
        logger.log("l", "Getting all users...")
        try:
            with self.sessionmaker_local.begin() as session:
                statement = select(User)
                users = session.execute(statement)
                users_result = users.scalars()
                users = []
                for user in users_result:
                    # print(user.userId)
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

        :param userId: uuid4 of user
        :type userId: Optional[str]

        :param email: email of user
        :type email: Optional[str]

        :param nickname: nickname of user
        :type nickname: Optional[str]


        :return: Json user info
        :rtype: dict
        """
        if userId is None and email is None and nickname is None:
            logger.log(
                "e",
                "At least of argument should be not None while calling `get_user`. Please, select userId/email/nickname",
            )
            return None

        logger.log("l", "Getting user...")

        conditions = []
        if userId is not None:
            conditions.append(User.userId == userId)
        if email is not None:
            conditions.append(User.email == email)
        if nickname is not None:
            conditions.append(User.nickname == nickname)

        # print(f"NICKNAME: {nickname}")e

        try:
            with self.sessionmaker_local.begin() as session:
                statement = select(User).where(*conditions)
                logger.log("i", f"Executing statement {nickname}")
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

    def delete_user(self, userId: str) -> status:
        logger.log("i", "Deleting user...")
        try:
            with self.sessionmaker_local.begin() as session:
                statement = delete(User).where(User.userId == userId)
                session.execute(statement)
                logger.log("i", "Deleted successfully")
                return status.HTTP_200_OK

        except Exception as e:
            logger.log(
                "e", f"An exception occured while deleting user. Full exception: {e}"
            )
            return status.HTTP_500_INTERNAL_SERVER_ERROR

    def create_user(self, email: str, nickname: str) -> Tuple[str, int]:
        logger.log(
            "i", f"Creating user with fields: email={email}, nickname={nickname}"
        )
        try:
            with self.sessionmaker_local.begin() as session:
                statement = insert(User).values(
                    userId=str(uuid4()),
                    email=email,
                    nickname=nickname,
                    createdAt=datetime.now(),
                    updatedAt=datetime.now(),
                    avatar=f"/img/avatars/{DEFAULT_AVATAR}".encode("utf-8"),
                )
                session.execute(statement)
                return "", status.HTTP_200_OK
        except Exception as e:
            logger.log(
                "e", f"Something went wrong while creating user. Full exception: {e}"
            )
            return e, status.HTTP_400_BAD_REQUEST
