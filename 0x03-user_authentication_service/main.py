#!/usr/bin/env python3
""" Testing Module
"""
import requests

BASE_URL = "http://localhost:5000"


def register_user(email: str, password: str) -> None:
    """Register a new user."""
    url = f"{BASE_URL}/register"
    data = {"email": email, "password": password}
    response = requests.post(url, json=data)
    assert response.status_code == 200
    print(f"User {email} registered successfully.")


def log_in_wrong_password(email: str, password: str) -> None:
    """Attempt to log in with an incorrect password."""
    url = f"{BASE_URL}/login"
    data = {"email": email, "password": password}
    response = requests.post(url, json=data)
    assert response.status_code == 401
    print(f"Failed login attempt for user {email} with incorrect password.")


def log_in(email: str, password: str) -> str:
    """Log in a user and return the session ID."""
    url = f"{BASE_URL}/login"
    data = {"email": email, "password": password}
    response = requests.post(url, json=data)
    assert response.status_code == 200
    session_id = response.json().get("session_id")
    print(f"User {email} logged in successfully. Session ID: {session_id}")
    return session_id


def profile_unlogged() -> None:
    """Retrieve the profile of an unlogged user."""
    url = f"{BASE_URL}/profile"
    response = requests.get(url)
    assert response.status_code == 401
    print("Profile retrieval for unlogged user failed (as expected).")


def profile_logged(session_id: str) -> None:
    """Retrieve the profile of a logged user."""
    url = f"{BASE_URL}/profile"
    headers = {"session_id": session_id}
    response = requests.get(url, headers=headers)
    assert response.status_code == 200
    print("Profile retrieved successfully.")


def log_out(session_id: str) -> None:
    """Log out a user."""
    url = f"{BASE_URL}/logout"
    headers = {"session_id": session_id}
    response = requests.delete(url, headers=headers)
    assert response.status_code == 200
    print("User logged out successfully.")


def reset_password_token(email: str) -> str:
    """Retrieve password reset token."""
    url = f"{BASE_URL}/reset_password"
    data = {"email": email}
    response = requests.post(url, json=data)
    assert response.status_code == 200
    reset_token = response.json().get("reset_token")
    print(f"Password reset token retrieved successfully: {reset_token}")
    return reset_token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Update a user's password."""
    url = f"{BASE_URL}/reset_password"
    data = {"email": email, "reset_token": reset_token,
            "new_password": new_password}
    response = requests.put(url, json=data)
    assert response.status_code == 200
    print("Password updated successfully.")


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
