#!/usr/bin/env python3
""" Encrypt password """
import bcrypt


def hash_password(password: str) -> bytes:
    """Returns a hashed password"""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Validates that the provided password matches the hashed password"""
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password)
