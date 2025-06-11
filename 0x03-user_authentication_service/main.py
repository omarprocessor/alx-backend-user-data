#!/usr/bin/env python3
"""
Main module for testing the user authentication service.
Uses `requests` to interact with the Flask app.
Each function corresponds to a user authentication feature.
"""

import requests

BASE_URL = "http://localhost:5000"


def register_user(email: str, password: str) -> None:
    """
    Registers a new user with the given email and password.
    Asserts that the user is successfully created or already exists.

    Args:
        email (str): The user's email.
        password (str): The user's password.
    """
    response = requests.post(f"{BASE_URL}/users",
                             data={'email': email, 'password': password})
    assert response.status_code in (200, 400)
    if response.status_code == 200:
        assert response.json() == {"email": email, "message": "user created"}
    else:
        assert response.json() == {"message": "email already registered"}


def log_in_wrong_password(email: str, password: str) -> None:
    """
    Attempts to log in with a wrong password and asserts failure.

    Args:
        email (str): The user's email.
        password (str): The incorrect password.
    """
    response = requests.post(f"{BASE_URL}/sessions",
                             data={'email': email, 'password': password})
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """
    Logs in a user and returns the session ID.

    Args:
        email (str): The user's email.
        password (str): The user's password.

    Returns:
        str: The session ID from the response cookie.
    """
    response = requests.post(f"{BASE_URL}/sessions",
                             data={'email': email, 'password': password})
    assert response.status_code == 200
    assert "session_id" in response.cookies
    return response.cookies["session_id"]


def profile_unlogged() -> None:
    """
    Attempts to access the profile without being logged in.
    Asserts that the request is forbidden.
    """
    response = requests.get(f"{BASE_URL}/profile")
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """
    Accesses the user's profile while logged in.

    Args:
        session_id (str): The user's session ID cookie.
    """
    cookies = {'session_id': session_id}
    response = requests.get(f"{BASE_URL}/profile", cookies=cookies)
    assert response.status_code == 200
    assert "email" in response.json()


def log_out(session_id: str) -> None:
    """
    Logs the user out using the session ID.

    Args:
        session_id (str): The user's session ID cookie.
    """
    cookies = {'session_id': session_id}
    response = requests.delete(f"{BASE_URL}/sessions", cookies=cookies)
    assert response.status_code == 200


def reset_password_token(email: str) -> str:
    """
    Requests a password reset token for the given email.

    Args:
        email (str): The user's email.

    Returns:
        str: The reset token returned by the server.
    """
    response = requests.post(f"{BASE_URL}/reset_password",
                             data={'email': email})
    assert response.status_code == 200
    json = response.json()
    assert "reset_token" in json
    return json["reset_token"]


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """
    Updates the user's password using the reset token.

    Args:
        email (str): The user's email.
        reset_token (str): The token to validate password reset.
        new_password (str): The new password to set.
    """
    data = {'email': email, 'reset_token': reset_token,
                            'new_password': new_password}
    response = requests.put(f"{BASE_URL}/reset_password", data=data)
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "Password updated"}


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
