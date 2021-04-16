import jwt
import os


def generate_token(username, **kwargs):
    encoded = jwt.encode(
        {"user": username},
        os.environ['SECRET_KEY_JWT'],
        algorithm="HS256",
    )
    return encoded

print('loco esto no esta andnado y no se porque')
x = list(range(10))
for i in x:
    print(i)