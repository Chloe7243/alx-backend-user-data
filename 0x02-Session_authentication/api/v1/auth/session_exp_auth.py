#!/usr/bin/env python3
""" Session Authentication Module (Expiration)
"""
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
from os import getenv


class SessionExpAuth(SessionAuth):
    """ Session Expiration Authentication Class
    """
    def __init__(self):
        """ Constructor
        """
        self.session_duration = int(getenv('SESSION_DURATION', 0))

    def create_session(self, user_id: str = None) -> str:
        """ Creates a session
        """
        session_id = super().create_session(user_id)
        if session_id:
            self.user_id_by_session_id[session_id] = {
                'user_id': user_id,
                'created_at': datetime.now()
            }
            return session_id
        return None

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ Returns user id based on a session id
        """
        if session_id and session_id in self.user_id_by_session_id:
            session_dict = self.user_id_by_session_id.get(session_id)
            if session_dict:
                if 'created_at' in session_dict:
                    if self.session_duration > 0:
                        if (session_dict['created_at'] +
                                timedelta(seconds=self.session_duration) <
                                datetime.now()):
                            return None
                    return session_dict.get('user_id')
            return None
