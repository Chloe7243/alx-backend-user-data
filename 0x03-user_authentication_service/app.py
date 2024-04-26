#!/usr/bin/env python3
""" Flask App
"""
from flask import Flask, jsonify, request, abort, redirect
from os import getenv
from auth import Auth


app = Flask(__name__)
app.url_map.strict_slashes = False
AUTH = Auth()


@app.route("/", methods=["GET"])
def hello() -> str:
    """ GET /
        Return:
          - JSON payload
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def register_user() -> str:
    """ POST /users
        Return:
          - JSON payload
    """
    try:
        email = request.form["email"]
        password = request.form["password"]
    except KeyError:
        abort(400)

    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"])
def log_in() -> str:
    """ POST /sessions
        Return:
          - JSON payload
    """
    try:
        email = request.form["email"]
        password = request.form["password"]
    except KeyError:
        abort(400)

    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        response = jsonify({"email": email, "message": "logged in"})
        response.set_cookie("session_id", session_id)
        return response
    else:
        abort(401)


@app.route("/sessions", methods=["DELETE"])
def log_out() -> str:
    """ DELETE /sessions
        Return:
          - JSON payload
    """
    try:
        session_id = request.cookies.get("session_id")
        user = AUTH.get_user_from_session_id(session_id)
        AUTH.destroy_session(user.id)
        return redirect("/")
    except Exception:
        abort(403)


@app.route("/profile", methods=["GET"])
def profile() -> str:
    """ GET /profile
        Return:
          - JSON payload
    """
    try:
        session_id = request.cookies.get("session_id")
        user = AUTH.get_user_from_session_id(session_id)
        return jsonify({"email": user.email}), 200
    except Exception:
        abort(403)


@app.route("/reset_password", methods=["POST"])
def get_reset_password_token() -> str:
    """ POST /reset_password
        Return:
          - JSON payload
    """
    try:
        email = request.form["email"]
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": reset_token}), 200
    except Exception:
        abort(403)


@app.route("/reset_password", methods=["PUT"])
def update_password() -> str:
    """ PUT /reset_password
        Return:
          - JSON payload
    """
    try:
        email = request.form["email"]
        reset_token = request.form["reset_token"]
        new_password = request.form["new_password"]
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"}), 200
    except Exception:
        abort(403)


if __name__ == "__main__":
    port = getenv("API_PORT") or 5000
    host = getenv("API_HOST") or "0.0.0.0"
    app.run(host=host, port=port)
