from .models import Bot
from development.encode_jwt import encode_data


def create_bot(strategy, user, response, is_new=False, *args, **kwargs):
    if not Bot.objects.filter(user=user,).exists():
        Bot.objects.create(
            name=user.email,
            token=encode_data(
                key='user',
                value=user.email,
            ),
            user=user,
        )

    return {
        'is_new': is_new,
        'user': user
    }
