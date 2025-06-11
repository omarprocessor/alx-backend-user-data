#!/usr/bin/env python3
"""
DB module to wrap SQLAlchemy session and database operations
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from typing import Optional, Any

from user import Base, User


class DB:
    """
    DB class for database operations using SQLAlchemy.
    """
    def __init__(self) -> None:
        """
        Initialize a new DB instance with an SQLite database.
        """
        self._engine = create_engine('sqlite:///a.db', echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """
        Return a memoized session object, creating it if necessary.
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Create a new user, add to the database, and return the User object.
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs: Any) -> User:
        """
        Find the first user matching the provided
        attributes; raise if not found.
        """
        query = self._session.query(User)
        for key, value in kwargs.items():
            if not hasattr(User, key):
                raise InvalidRequestError
            query = query.filter(getattr(User, key) == value)
        user = query.one()
        return user

    def update_user(self, user_id: int, **kwargs: Any) -> None:
        """
        Update user attributes and commit; raise if any attribute invalid.
        """
        user = self.find_user_by(id=user_id)
        for key, value in kwargs.items():
            if not hasattr(user, key):
                raise ValueError
            setattr(user, key, value)
        self._session.commit()
