from django.contrib import messages
import jwt
import os


SECRET_KEY = 'EDAGame$!2021'


def show_token(user, request, **kwargs):
    encoded = jwt.encode(
        {"user": user.username},
        os.environ['SECRET_KEY_JWT'],
        algorithm="HS256",
    )
    messages.success(
        request,
        f'Token: {encoded}',
    )
