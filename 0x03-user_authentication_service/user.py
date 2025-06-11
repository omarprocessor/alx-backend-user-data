#!/usr/bin/env python3
"""
User model that represents a user in the database.
This model defines the structure of the users table and provides methods
for interacting with user data.
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    """
    User class that represents a user in the database.

    Attributes:
        id: Primary key
        email: User's email address
        hashed_password: Hashed password
        session_id: Session ID for user's current session
        reset_token: Token for password reset
    """

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)
