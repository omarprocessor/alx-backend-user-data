#!/usr/bin/env python3
"""
Module that provides a function to hash a password using bcrypt
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
