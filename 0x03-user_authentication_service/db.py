#!/usr/bin/env python3
"""
DB module
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

from user import Base, User


class DB:
    """
    DB class to handle database operations.

    Attributes:
        _engine: SQLAlchemy engine instance
        _session: SQLAlchemy session instance
    """

    def __init__(self) -> None:
        """
        Initialize a new DB instance.
        Creates a new SQLite database and sets up tables.
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """
        Get a memoized session object.

        Returns:
            Session: SQLAlchemy session instance
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Add a new user to the database.

        Args:
            email: User's email address
            hashed_password: Hashed password

        Returns:
            User: The newly created user object
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """
        Find a user by arbitrary keyword arguments.

        Args:
            **kwargs: Arbitrary keyword arguments for filtering

        Returns:
            User: First matching user object

        Raises:
            NoResultFound: If no user is found
            InvalidRequestError: If invalid query arguments are passed
        """
        try:
            query = self._session.query(User)
            for key, value in kwargs.items():
                query = query.filter(getattr(User, key) == value)
            return query.first()
        except NoResultFound:
            raise
        except InvalidRequestError:
            raise

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Update a user's attributes.

        Args:
            user_id: ID of the user to update
            **kwargs: Arbitrary keyword arguments for updating user attributes

        Raises:
            ValueError: If an invalid attribute is passed
        """
        try:
            user = self.find_user_by(id=user_id)
            for key, value in kwargs.items():
                if hasattr(user, key):
                    setattr(user, key, value)
                else:
                    raise ValueError(f"Invalid attribute: {key}")
            self._session.commit()
        except NoResultFound:
            raise ValueError(f"User with ID {user_id} not found")
