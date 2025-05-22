#!/usr/bin/env python3
"""
Module that provides functions to hash and validate passwords using bcrypt
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hash a password using bcrypt with a salt

    Args:
        password (str): The password to hash

    Returns:
        bytes: The salted, hashed password
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Validate a password against the hashed version using bcrypt

    Args:
        hashed_password (bytes): The hashed password
        password (str): The plain text password to validate

    Returns:
        bool: True if valid, False otherwise
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
