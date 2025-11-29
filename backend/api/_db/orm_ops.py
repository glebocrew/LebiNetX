from sqlalchemy import create_engine, select, delete, insert, update
from sqlalchemy.orm import sessionmaker
from typing import List, Optional, Dict, Tuple
from consts import DEFAULT_AVATAR

from fastapi import status

from _db.PASSWORDS import HOST, PORT, USER, PASSWORD, DATABASE
from _db.db_models import User, Post

from hashlib import sha512

from logger import Logger
from uuid import uuid4
from datetime import datetime

logger = Logger("logs/db_logs.txt")


class DataBase:
    def __init__(self):
        self.engine = create_engine(
            f"mariadb+mariadbconnector://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
        )

        self.sessionmaker_local = sessionmaker(
            autoflush=False, autocommit=False, bind=self.engine
        )

    # ============================================
    #                    USERS
    # ============================================

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
                            "pwd": user.pwd,
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
                logger.log("i", f"Executing statement {statement}")
                user = session.execute(statement).scalar()

                return {
                    "userId": user.userId,
                    "nickname": user.nickname,
                    "email": user.email,
                    "pwd": user.pwd,
                    "createdAt": user.createdAt,
                    "updatedAt": user.updatedAt,
                    "avatar": user.avatar,
                }

        except Exception as e:
            logger.log(
                "e", f"The operation of getting user was incomplete! Full exception {e}"
            )

    def delete_user(self, userId: str) -> status:
        """
        Deletes user only by id

        :param userId: uuid4 of user
        :type userId: str
        :return: HTTP status of the action
        :rtype: status
        """
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

    def create_user(self, email: str, nickname: str, pwd: str) -> Tuple[str, int]:
        logger.log(
            "i",
            f"Creating user with fields: email={email}, nickname={nickname}, password={pwd}",
        )
        try:
            with self.sessionmaker_local.begin() as session:
                password = sha512()
                password.update(str.encode(pwd, "utf-8"))
                pwd = password.hexdigest()

                statement = insert(User).values(
                    userId=str(uuid4()),
                    email=email,
                    nickname=nickname,
                    pwd=pwd,
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
            return str(e).split(sep=":")[0], status.HTTP_400_BAD_REQUEST

    def patch_user(
        self,
        userId: str,
        email: Optional[str] = None,
        nickname: Optional[str] = None,
        password: Optional[str] = None,
    ) -> Optional[Tuple]:
        """
        Patches one user

        :param userId: uuid4 of user
        :type userId: str

        :param email: email of user [NEW]
        :type email: Optional[str]

        :param nickname: nickname of user [NEW]
        :type nickname: Optional[str]

        :param password: password of user [NEW]
        :type password: Optional[str]

        :return: status of patch
        :rtype: tuple
        """
        if email is None and nickname is None and password is None:
            logger.log(
                "e",
                "At least of argument should be not None while calling `patch_user`. Please, select email/nickname/pwd",
            )
            return "No arguments", status.HTTP_400_BAD_REQUEST

        logger.log("l", "Patching user...")

        values = {}
        if email is not None:
            values["email"] = email
        if nickname is not None:
            values["nickname"] = nickname
        if password is not None:
            values["pwd"] = password
            pwd = sha512()
            pwd.update(str.encode(values["pwd"], "utf-8"))
            values["pwd"] = pwd.hexdigest()
        values["updatedAt"] = datetime.now()
        # print(f"{values['pwd']}")

        try:
            with self.sessionmaker_local.begin() as session:
                statement = update(User).where(User.userId == userId).values(**values)
                logger.log("i", f"Executing statement {statement}")
                session.execute(statement)
                return "", status.HTTP_200_OK

        except Exception as e:
            logger.log(
                "e",
                f"The operation of patching user was incomplete! Full exception {e}",
            )
            return str(e).split(sep=":")[0], status.HTTP_400_BAD_REQUEST

    # ============================================
    #                    POSTS
    # ============================================

    def get_posts(self) -> List[Dict]:
        """
        Gets all posts

        :returns: List of Posts
        :rtype: List[Dict]
        """
        logger.log("i", "Getting all posts...")
        try:
            with self.sessionmaker_local.begin() as session:
                statement = select(Post)
                logger.log("i", f"Executing statiement: {statement}")
                result = session.execute(statement).scalars()
                if result == []:
                    return None

                posts = []
                for post in result:
                    posts.append(
                        {
                            "postId": post.postId,
                            "userId": post.userId,
                            "title": post.title,
                            "content": post.content,
                            "createdAt": post.createdAt,
                            "updatedAt": post.updatedAt,
                        }
                    )
                print(result)
                return posts
        except Exception as e:
            logger.log("e", f"An exception occured! E: {e}")

    def get_user_posts(self, userId):
        """
        Gets user's posts

        :returns: List of Posts
        :rtype: Dict
        """
        logger.log("i", "Getting all user's posts...")
        try:
            with self.sessionmaker_local.begin() as session:
                statement = select(Post).where(Post.userId == userId)
                logger.log("i", f"Executing statiement: {statement}")
                result = session.execute(statement).scalars()
                print(result)
                if result == []:
                    return None

                posts = []
                for post in result:
                    posts.append(
                        {
                            "postId": post.postId,
                            "userId": post.userId,
                            "title": post.title,
                            "content": post.content,
                            "createdAt": post.createdAt,
                            "updatedAt": post.updatedAt,
                        }
                    )

                return posts
        except Exception as e:
            logger.log("e", f"An exception occured! E: {e}")

    def create_post(self, userId: str, title: str, content: str) -> Tuple[str, int]:
        logger.log("i", "Creating post...")
        try:
            with self.sessionmaker_local.begin() as session:
                statement = insert(Post).values(
                    postId=str(uuid4()),
                    userId=userId,
                    title=title,
                    content=content,
                    createdAt=datetime.now(),
                    updatedAt=datetime.now(),
                )

                session.execute(statement)
                return ("", status.HTTP_200_OK)

        except Exception as e:
            logger.log(
                "e", f"Something went wrong while creating post. Full exception: {e}"
            )
            return (str(e).split(sep=":")[0], status.HTTP_400_BAD_REQUEST)

    def delete_post(self, postId):
        """
        Deletes post only by id

        :param userId: uuid4 of post
        :type userId: str
        :return: HTTP status of the action
        :rtype: status
        """
        logger.log("i", "Deleting post...")
        try:
            with self.sessionmaker_local.begin() as session:
                statement = delete(Post).where(Post.postId == postId)
                session.execute(statement)
                logger.log("i", "Deleted successfully")
                return status.HTTP_200_OK

        except Exception as e:
            logger.log(
                "e", f"An exception occured while deleting post. Full exception: {e}"
            )
            return status.HTTP_500_INTERNAL_SERVER_ERROR

    def patch_post(
        self,
        postId: str,
        title: Optional[str] = None,
        content: Optional[str] = None,
    ) -> Optional[Tuple]:
        """
        Patches post

        :param userId: uuid4 of post
        :type userId: str

        :param title: title of post [NEW]
        :type title: Optional[str]

        :param content: content of post [NEW]
        :type content: Optional[str]

        :return: status of patch
        :rtype: tuple
        """
        if title is None and content is None:
            logger.log(
                "e",
                "At least of argument should be not None while calling `patch_post`. Please, select title/content",
            )
            return "No arguments", status.HTTP_400_BAD_REQUEST

        logger.log("l", "Patching post...")

        values = {}
        if title is not None:
            values["title"] = title
        if content is not None:
            values["content"] = content
        values["updatedAt"] = datetime.now()

        try:
            with self.sessionmaker_local.begin() as session:
                statement = update(Post).where(Post.postId == postId).values(**values)
                logger.log("i", f"Executing statement {statement}")
                session.execute(statement)
                return "", status.HTTP_200_OK

        except Exception as e:
            logger.log(
                "e",
                f"The operation of patching post was incomplete! Full exception {e}",
            )
            return str(e).split(sep=":")[0], status.HTTP_400_BAD_REQUEST
