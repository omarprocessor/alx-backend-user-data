#!/usr/bin/env python3
"""
Main Flask application for user authentication service.
"""

from flask import Flask, jsonify, request, abort
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'])
def welcome():
    """
    Welcome endpoint.

    Returns:
        JSON: Welcome message
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def register_user():
    """
    Register a new user.

    Request body should contain:
    - email: user's email address
    - password: user's password

    Returns:
        JSON: User info if registration is successful
        400: If email is already registered
    """
    try:
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            abort(400)

        user = AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"}), 200
    except ValueError as e:
        abort(400, description=str(e))


@app.route('/sessions', methods=['POST'])
def login():
    """
    Create a new session for a user.

    Request body should contain:
    - email: user's email address
    - password: user's password

    Returns:
        JSON: Session info if login is successful
        401: If credentials are invalid
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        abort(401)

    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        response = jsonify({"email": email, "message": "logged in"})
        response.set_cookie('session_id', session_id)
        return response

    abort(401)


@app.route('/sessions', methods=['DELETE'])
def logout():
    """
    Logout the user and destroy the session.

    Returns:
        302: Redirect to root URL if successful
        403: If session is invalid
    """
    session_id = request.cookies.get('session_id')
    if not session_id:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)

    AUTH.destroy_session(user.id)
    response = jsonify({"message": "logout successful"})
    response.delete_cookie('session_id')
    return response, 302


@app.route('/profile', methods=['GET'])
def profile():
    """
    Get the user's profile information.

    Returns:
        JSON: User info if successful
        403: If session is invalid
    """
    session_id = request.cookies.get('session_id')
    if not session_id:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)

    return jsonify({"email": user.email})


@app.route('/reset_password', methods=['POST'])
def reset_password():
    """
    Generate a reset password token.

    Request body should contain:
    - email: user's email address

    Returns:
        JSON: Reset token info if successful
        403: If user not found
    """
    email = request.form.get('email')
    if not email:
        abort(403)

    try:
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": reset_token})
    except ValueError:
        abort(403)


@app.route('/reset_password', methods=['PUT'])
def update_password():
    """
    Update user's password using reset token.

    Request body should contain:
    - email: user's email address
    - reset_token: reset token
    - new_password: new password

    Returns:
        JSON: Success message if password is updated
        403: If token is invalid
    """
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')

    if not email or not reset_token or not new_password:
        abort(403)

    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"})
    except ValueError:
        abort(403)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
