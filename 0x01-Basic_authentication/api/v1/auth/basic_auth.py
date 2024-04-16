#!/usr/bin/env python3
""" Basic User Authentication Module
"""
from api.v1.auth.auth import Auth
from models.user import User
from base64 import b64decode
from flask import request
from typing import List, TypeVar


class BasicAuth(Auth):
    """ Basic Authentication Class
    """

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """ Extracts Base64 Authorization Header
        """

        auth = authorization_header
        if auth and type(auth) is str and auth.startswith("Basic "):
            return auth.split(" ")[1]

        return None

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """ Decode Base64 Authorization Header
        """
        b64auth = base64_authorization_header
        if b64auth and type(b64auth) is str:
            try:
                decoded = b64decode(b64auth.encode('utf-8'))
                return decoded.decode('utf-8')
            except Exception:
                return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """ Extract User Credentials
        """
        auth = decoded_base64_authorization_header
        if auth and type(auth) is str and ':' in auth:
            return auth.split(":", 1)
        return (None, None)

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """ Get User object from Credentials
        """
        if not user_email and not type(user_email) is str:
            return None
        if not user_pwd and not type(user_pwd) is str:
            return None

        try:
            found_users = User.search({"email": user_email})
        except Exception:
            return None

        for user in found_users:
            if user.is_valid_password(user_pwd):
                return user

        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Get current user object
        """
        auth = self.authorization_header(request)
        extracted_base64 = self.extract_base64_authorization_header(auth)
        decoded = self.decode_base64_authorization_header(extracted_base64)
        email, pwd = self.extract_user_credentials(decoded)
        user = self.user_object_from_credentials(email, pwd)
        return user
