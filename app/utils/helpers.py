from flask import jsonify


def ok(data=None, status=200):
    return jsonify(data or {})

def bad(message="bad request", status=400):
    return jsonify({"message": message}), status
