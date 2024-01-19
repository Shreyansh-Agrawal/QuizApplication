"""Functions to handle errors"""

from flask import jsonify


def handle_internal_server_error(_err):
    """Function to handle server side errors"""

    return jsonify({"code": 500, "status": "An error occured at the server!"}), 500
