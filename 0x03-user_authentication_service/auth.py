#!/usr/bin/env python3
"""
Auth class to handle user authentication and session management.
"""

import bcrypt
import uuid
from typing import Optional
from db import DB
from user import User


class Auth:
    """
    Auth class to register, login, session, and password reset operations.
    """
    def __init__(self) -> None:
        """
        Initialize Auth with a DB instance.
        """
        self._db = DB()

    def _hash_password(self, password: str) -> bytes:
        """
        Hash a password using bcrypt and return the salt+hash bytes.
        """
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    def register_user(self, email: str, password: str) -> User:
        """
        Register a new user; raise if user already exists.
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except Exception:
            hashed = self._hash_password(password)
            return self._db.add_user(email, hashed.decode('utf-8'))

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validate login credentials; return True if correct, False otherwise.
        """
        try:
            user = self._db.find_user_by(email=email)
        except Exception:
            return False
        return bcrypt.checkpw(password.encode('utf-8'),
                              user.hashed_password.encode('utf-8'))

    def _generate_uuid(self) -> str:
        """
        Generate a new UUID string.
        """
        return str(uuid.uuid4())

    def create_session(self, email: str) -> Optional[str]:
        """
        Create a new session ID for a user
        and return it; None if user not found.
        """
        try:
            user = self._db.find_user_by(email=email)
        except Exception:
            return None
        session_id = self._generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> Optional[User]:
        """
        Return the User associated with session_id, or None if invalid.
        """
        if not session_id:
            return None
        try:
            return self._db.find_user_by(session_id=session_id)
        except Exception:
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        Invalidate a user's session by setting their session_id to None.
        """
        try:
            self._db.update_user(user_id, session_id=None)
        except Exception:
            pass

    def get_reset_password_token(self, email: str) -> str:
        """
        Generate and store a reset token for a user, return the token.
        """
        try:
            user = self._db.find_user_by(email=email)
        except Exception:
            raise ValueError
        token = self._generate_uuid()
        self._db.update_user(user.id, reset_token=token)
        return token

    def update_password(self, reset_token: str, password: str) -> None:
        """
        Update a user's password using reset_token; invalidate the reset_token.
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except Exception:
            raise ValueError
        hashed = self._hash_password(password).decode('utf-8')
        self._db.update_user(user.id,
                             hashed_password=hashed,
                             reset_token=None)
