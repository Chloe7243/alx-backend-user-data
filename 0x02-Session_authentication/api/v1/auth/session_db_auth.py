#!/usr/bin/env python3
""" Session Authentication Module (Database)
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """ Session Database Authentication Class
    """
    def create_session(self, user_id: str = None) -> str:
        """ Creates a session
        """
        session_id = super().create_session(user_id)
        if session_id:
            session = UserSession(user_id=user_id, session_id=session_id)
            session.save()
            UserSession.save_to_file()
            return session_id
        return None

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ Returns user id based on a session id
        """
        if session_id:
            UserSession.load_from_file()
            session = UserSession.search({'session_id': session_id})
            if session:
                if self.session_duration > 0:
                    if (session[0].created_at +
                            timedelta(seconds=self.session_duration) <
                            datetime.now()):
                        return None
                return session[0].user_id
        return None

    def destroy_session(self, request=None):
        """ Deletes the user session / logout
        """
        if request:
            session_id = self.session_cookie(request)
            if session_id:
                UserSession.load_from_file()
                session = UserSession.search({'session_id': session_id})
                if session:
                    session[0].remove()
                    UserSession.save_to_file()
                    return True
        return False
