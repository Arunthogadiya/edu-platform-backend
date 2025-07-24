from flask_jwt_extended import JWTManager, create_access_token as jwt_create_access_token, create_refresh_token as jwt_create_refresh_token, decode_token as jwt_decode_token
from datetime import timedelta

class Auth:
    def __init__(self, app):
        self.jwt = JWTManager(app)

    @staticmethod
    def create_access_token(identity, expires_delta=timedelta(minutes=30)):
        """Create an access token."""
        return jwt_create_access_token(identity=identity, expires_delta=expires_delta)

    @staticmethod
    def create_refresh_token(identity):
        """Create a refresh token."""
        return jwt_create_refresh_token(identity=identity)

    @staticmethod
    def decode_token(token):
        """Decode a token."""
        return jwt_decode_token(token)
