import jwt
import os


def generate_token(email, **kwargs):
    encoded = jwt.encode(
        {"user": email},
        os.environ['SECRET_KEY_JWT'],
        algorithm="HS256",
    )
    return encoded
