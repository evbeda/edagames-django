from django.contrib import messages
import jwt

SECRET_KEY = 'EDAGame$!2021'


def show_token(user, request, **kwargs):
    encoded = jwt.encode({"user": user.username}, SECRET_KEY, algorithm="HS256")
    messages.success(
        request,
        f'Token: {encoded}',
    )
