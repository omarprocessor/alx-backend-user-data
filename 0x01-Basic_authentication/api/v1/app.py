#!/usr/bin/env python3
"""
This module initializes the Flask application and handles errors.
"""

from flask import Flask, jsonify
from api.v1.views import app_views
from flask import Blueprint
from flask import abort

app = Flask(__name__)
app.register_blueprint(app_views)


@app.errorhandler(401)
def unauthorized_error(error):
    """
    Returns a JSON-formatted 401 Unauthorized error response.
    """
    return jsonify({"error": "Unauthorized"}), 401


if __name__ == "__main__":
    from os import getenv

    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=int(port), debug=True)
