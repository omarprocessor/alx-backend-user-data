#!/usr/bin/env python3
"""
Defines routes for index and custom error demonstration.
"""

from flask import jsonify
from api.v1.views import app_views
from flask import abort


@app_views.route('/api/v1/status', methods=['GET'], strict_slashes=False)
def status():
    """
    Returns API status.
    """
    return jsonify({"status": "OK"})


@app_views.route('/api/v1/unauthorized', methods=['GET'], strict_slashes=False)
def unauthorized():
    """
    Raises a 401 Unauthorized error for testing purposes.
    """
    abort(401)
