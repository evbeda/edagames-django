from .models import Bot
from development.token import generate_token


def create_bot(strategy, user, response, is_new=False, *args, **kwargs):
    # import ipdb; ipdb.set_trace()
    if not Bot.objects.filter(user=user,).exists():
        Bot.objects.create(
            name=user.username,
            token=generate_token(user.username),
            user=user,
        )

    return {
        'is_new': is_new,
        'user': user
    }
