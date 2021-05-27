import jwt
import os


def encode_data(*args, **kwargs):
    encoded = jwt.encode(
        {kwargs['key']: kwargs['value']},
        os.environ['SECRET_KEY_JWT'],
        algorithm="HS256",
    )
    return encoded
