import jwt
import os


def generate_token(username, **kwargs):
    encoded = jwt.encode(
        {"user": username},
        os.environ['SECRET_KEY_JWT'],
        algorithm="HS256",
    )
    return encoded
