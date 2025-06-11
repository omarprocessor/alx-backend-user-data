#!/usr/bin/env python3
"""
Authentication service that handles user authentication and session management.
"""

import bcrypt
from db import DB
from uuid import uuid4
from typing import Union


class Auth:
    """
    Auth class to interact with the authentication database.

    Attributes:
        _db: Database instance for database operations
    """

    def __init__(self):
        """
        Initialize a new Auth instance.
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Register a new user.

        Args:
            email: User's email address
            password: User's password

        Returns:
            User: The newly created user object

        Raises:
            ValueError: If user with given email already exists
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = _hash_password(password)
            return self._db.add_user(email, hashed_password)

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validate user credentials.

        Args:
            email: User's email address
            password: User's password

        Returns:
            bool: True if credentials are valid, False otherwise
        """
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(
                password.encode('utf-8'),
                user.hashed_password.encode('utf-8')
            )
        except (NoResultFound, InvalidRequestError):
            return False

    def create_session(self, email: str) -> Union[str, None]:
        """
        Create a new session for a user.

        Args:
            email: User's email address

        Returns:
            str: Session ID if successful, None if user not found
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except (NoResultFound, InvalidRequestError):
            return None

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """
        Get user from session ID.

        Args:
            session_id: Session ID

        Returns:
            User: User object if session is valid, None otherwise
        """
        if not session_id:
            return None
        try:
            return self._db.find_user_by(session_id=session_id)
        except (NoResultFound, InvalidRequestError):
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        Destroy a user's session.

        Args:
            user_id: User's ID
        """
        try:
            self._db.update_user(user_id, session_id=None)
        except ValueError:
            pass

    def get_reset_password_token(self, email: str) -> str:
        """
        Generate a reset password token for a user.

        Args:
            email: User's email address

        Returns:
            str: Reset password token

        Raises:
            ValueError: If user with given email does not exist
        """
        try:
            user = self._db.find_user_by(email=email)
            reset_token = _generate_uuid()
            self._db.update_user(user.id, reset_token=reset_token)
            return reset_token
        except (NoResultFound, InvalidRequestError):
            raise ValueError(f"User {email} not found")

    def update_password(self, reset_token: str, password: str) -> None:
        """
        Update user's password using reset token.

        Args:
            reset_token: Reset password token
            password: New password

        Raises:
            ValueError: If reset token is invalid
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            hashed_password = _hash_password(password)
            self._db.update_user(
                user.id,
                hashed_password=hashed_password,
                reset_token=None
            )
        except (NoResultFound, InvalidRequestError):
            raise ValueError("Invalid reset token")


def _hash_password(password: str) -> str:
    """
    Hash a password using bcrypt.

    Args:
        password: Password string

    Returns:
        str: Hashed password
    """
    return bcrypt.hashpw(password.encode('utf-8'),
                         bcrypt.gensalt()).decode('utf-8')


def _generate_uuid() -> str:
    """
    Generate a UUID string.

    Returns:
        str: UUID string
    """
    return str(uuid4())
