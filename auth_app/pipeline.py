from .models import Bot
from development.token import generate_token


def create_bot(strategy, user, response, is_new=False, *args, **kwargs):
    if not Bot.objects.filter(user=user,).exists():
        Bot.objects.create(
            name=user.email,
            token=generate_token(user.email),
            user=user,
        )

    return {
        'is_new': is_new,
        'user': user
    }
