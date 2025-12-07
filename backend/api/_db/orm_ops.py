from sqlalchemy import create_engine, select, delete, insert, update
from sqlalchemy.orm import sessionmaker
from typing import List, Optional, Dict, Tuple
from consts import DEFAULT_AVATAR

from fastapi import status

from _db.PASSWORDS import HOST, PORT, USER, PASSWORD, DATABASE
from _db.db_models import User, Post, PostReaction, Comment, CommentReaction, Hashtag

from _ai import generate_hashtags

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
        pwd: Optional[str] = None
    ) -> Optional[Dict]:
        """
        Gets one user

        :param userId: uuid4 of user
        :type userId: Optional[str]

        :param email: email of user
        :type email: Optional[str]

        :param nickname: nickname of user
        :type nickname: Optional[str]

        :param pwd: password hash of user
        :type pwd: Optional[str]


        :return: Json user info
        :rtype: dict
        """
        if userId is None and email is None and nickname is None and pwd is not None:
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
        if pwd is not None:
            password = sha512()
            password.update(str.encode(pwd, "utf-8"))
            pwd = password.hexdigest()
            
            conditions.append(User.pwd == pwd)

        # print(f"NICKNAME: {nickname}")e

        try:
            with self.sessionmaker_local.begin() as session:
                statement = select(User).where(*conditions)
                logger.log("i", f"Executing statement {statement}")
                user = session.execute(statement).scalar()
                if user:
                    return {
                        "userId": user.userId,
                        "nickname": user.nickname,
                        "email": user.email,
                        "pwd": user.pwd,
                        "createdAt": user.createdAt,
                        "updatedAt": user.updatedAt,
                        "avatar": user.avatar,
                    }
                else:
                    return None

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
                postId = str(uuid4())
                statement = insert(Post).values(
                    postId=postId,
                    userId=userId,
                    title=title,
                    content=content,
                    createdAt=datetime.now(),
                    updatedAt=datetime.now(),
                )

                session.execute(statement)

                for hashtag in generate_hashtags(content):
                    statement = insert(Hashtag).values(
                        hashtagId=str(uuid4()), postId=postId, hashtag=hashtag
                    )
                    session.execute(statement=statement)
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

    # ============================================
    #               POST_REACTIONS
    # ============================================

    def get_post_reactions(self, postId: str) -> List[Dict]:
        """
        Gets all post reactions

        :param postId: uuid of PostReaction
        :type postId: str

        :returns: List of Posts
        :rtype: List[Dict]
        """
        logger.log("i", "Getting all posts...")
        try:
            with self.sessionmaker_local.begin() as session:
                statement = select(PostReaction).where(PostReaction.postId == postId)
                logger.log("i", f"Executing statiement: {statement}")
                result = session.execute(statement).scalars()
                if result == []:
                    return None

                reactions = []
                for reaction in result:
                    reactions.append(
                        {
                            "reactionId": reaction.reactionId,
                            "postId": reaction.postId,
                            "userId": reaction.userId,
                            "reaction": reaction.reaction,
                        }
                    )
                print(result)
                return reactions
        except Exception as e:
            logger.log("e", f"An exception occured! E: {e}")

    def create_post_reaction(
        self, userId: str, postId: str, reaction: int
    ) -> Tuple[str, int]:
        """
        Creates a reaction on a post

        :param reactionId: uuid of reaction [PK]
        :type reactionId: str

        :param userId: uuid of user [FK]
        :type userId: str

        :param postId: uuid of post [FK]
        :type postId: str

        :param reaction: reaction number
        :type reaction: int
        """
        logger.log("i", "Creating post reaction...")
        try:
            with self.sessionmaker_local.begin() as session:
                statement = insert(PostReaction).values(
                    reactionId=str(uuid4()),
                    userId=userId,
                    postId=postId,
                    reaction=reaction,
                )

                logger.log("i", f"Executing statement {statement}")
                session.execute(statement)
                logger.log("i", "Succesfully created post reaction!")

                return "", status.HTTP_200_OK
        except Exception as e:
            logger.log(
                "e", f"An exception occured while creating new post reaction: {e}"
            )
            return str(e).split(sep=":")[0], status.HTTP_400_BAD_REQUEST

    def delete_post_reaction(self, reactionId):
        """
        Deletes post reaction only by id

        :param reactionId: uuid4 of post
        :type reactionId: str
        :return: HTTP status of the action
        :rtype: status
        """
        logger.log("i", "Deleting post reaction...")
        try:
            with self.sessionmaker_local.begin() as session:
                statement = delete(PostReaction).where(
                    PostReaction.postId == reactionId
                )
                session.execute(statement)
                logger.log("i", "Deleted successfully")
                return status.HTTP_200_OK

        except Exception as e:
            logger.log(
                "e",
                f"An exception occured while deleting post reaction. Full exception: {e}",
            )
            return status.HTTP_500_INTERNAL_SERVER_ERROR

    # ============================================
    #                  COMMENTS
    # ============================================

    def create_comment(self, userId: str, postId: str, content: str) -> Tuple[str, int]:
        logger.log("i", "Creating comment...")
        try:
            with self.sessionmaker_local.begin() as session:
                statement = insert(Comment).values()
                session.execute(statement)
                return ("", status.HTTP_200_OK)

        except Exception as e:
            logger.log(
                "e",
                f"Something went wrong while creating commment. Full exception: {e}",
            )
            return (str(e).split(sep=":")[0], status.HTTP_400_BAD_REQUEST)

    def get_comments(self, postId):
        """
        Gets all post reactions

        :param postId: uuid of Comment
        :type postId: str

        :returns: List of Comments
        :rtype: List[Dict]
        """
        logger.log("i", "Getting all comments...")
        try:
            with self.sessionmaker_local.begin() as session:
                statement = select(Comment).where(Comment.postId == postId)
                logger.log("i", f"Executing statiement: {statement}")
                result = session.execute(statement).scalars()
                if result == []:
                    return None

                comments = []
                for comment in result:
                    comments.append(
                        {
                            "commentId": comment.commentId,
                            "postId": comment.postId,
                            "userId": comment.userId,
                            "content": comment.content,
                        }
                    )
                print(result)
                return comments
        except Exception as e:
            logger.log("e", f"An exception occured! E: {e}")

    # ============================================
    #              COMMENT_REACTIONS
    # ============================================

    def get_comment_reactions(self, commentId: str) -> List[Dict]:
        """
        Gets all post reactions

        :param commentId: uuid of CommentReaction
        :type commentId: str

        :returns: List of CommentReactions
        :rtype: List[Dict]
        """
        logger.log("i", "Getting all comment reactions...")
        try:
            with self.sessionmaker_local.begin() as session:
                statement = select(CommentReaction).where(
                    CommentReaction.commentId == commentId
                )
                logger.log("i", f"Executing statiement: {statement}")
                result = session.execute(statement).scalars()
                if result == []:
                    return None

                reactions = []
                for reaction in result:
                    reactions.append(
                        {
                            "reactionId": reaction.reactionId,
                            "commentId": reaction.commentId,
                            "userId": reaction.userId,
                            "reaction": reaction.reaction,
                        }
                    )
                print(result)
                return reactions
        except Exception as e:
            logger.log("e", f"An exception occured! E: {e}")

    def create_comment_reaction(
        self, userId: str, commentId: str, reaction: int
    ) -> Tuple[str, int]:
        """
        Creates a reaction on a post

        :param reactionId: uuid of reaction [PK]
        :type reactionId: str

        :param userId: uuid of user [FK]
        :type userId: str

        :param commentId: uuid of comment [FK]
        :type postId: str

        :param reaction: reaction number
        :type reaction: int
        """
        logger.log("i", "Creating comment reaction...")
        try:
            with self.sessionmaker_local.begin() as session:
                statement = insert(CommentReaction).values(
                    reactionId=str(uuid4()),
                    userId=userId,
                    commentId=commentId,
                    reaction=reaction,
                )

                logger.log("i", f"Executing statement {statement}")
                session.execute(statement)
                logger.log("i", "Succesfully created comment reaction!")

                return "", status.HTTP_200_OK
        except Exception as e:
            logger.log(
                "e", f"An exception occured while creating new comment reaction: {e}"
            )
            return str(e).split(sep=":")[0], status.HTTP_400_BAD_REQUEST

    def delete_comment_reaction(self, reactionId):
        """
        Deletes comment reaction only by id

        :param reactionId: uuid4 of post
        :type reactionId: str
        :return: HTTP status of the action
        :rtype: status
        """
        logger.log("i", "Deleting comment reaction...")
        try:
            with self.sessionmaker_local.begin() as session:
                statement = delete(CommentReaction).where(
                    CommentReaction.postId == reactionId
                )
                session.execute(statement)
                logger.log("i", "Deleted successfully")
                return status.HTTP_200_OK

        except Exception as e:
            logger.log(
                "e",
                f"An exception occured while deleting comment reaction. Full exception: {e}",
            )
            return status.HTTP_500_INTERNAL_SERVER_ERROR

    # ============================================
    #                HASHTAGS
    # ============================================

    def get_hashtags(self, postId):
        """
        Gets post's hashtags

        :returns: List of Posts
        :rtype: Dict
        """
        logger.log("i", "Getting all post's hashtags...")
        try:
            with self.sessionmaker_local.begin() as session:
                statement = select(Hashtag).where(Hashtag.postId == postId)
                logger.log("i", f"Executing statiement: {statement}")
                result = session.execute(statement).scalars()
                print(result)
                if result == []:
                    return None

                hashtags = []
                for hashtag in result:
                    hashtags.append(
                        {
                            "hashtagId": hashtag.hashtagId,
                            "postId": hashtag.postId,
                            "hashtag": hashtag.hashtag,
                        }
                    )

                return hashtags
        except Exception as e:
            logger.log("e", f"An exception occured! E: {e}")
