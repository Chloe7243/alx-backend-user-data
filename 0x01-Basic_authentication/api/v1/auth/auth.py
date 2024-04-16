#!/usr/bin/env python3
""" User Authentication Module
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """ Authentication Class
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Checks if a path requires Authentication
        """
        if path and excluded_paths:
            for ex_path in excluded_paths:
                if path[:(len(ex_path) - 1)] == ex_path[:-1]:
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        """ Returns the Authorization Header
        """
        if request:
            return request.headers.get("Authorization", None)
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Current User
        """
        return None
