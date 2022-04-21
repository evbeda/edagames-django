from .models import Bot


def create_bot(strategy, user, response, is_new=False, *args, **kwargs):
    if not Bot.objects.filter(user=user,).exists():
        Bot.objects.create(
            name=user.email,
            user=user,
        )

    return {
        'is_new': is_new,
        'user': user
    }
