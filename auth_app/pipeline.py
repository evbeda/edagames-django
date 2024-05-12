import requests
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


def fill_user(strategy, user, response, is_new=False, *args, **kwargs):
    social = user.social_auth.get()
    headers = {
        'Authorization': f'Bearer {social.access_token}',
        'Connection': 'Keep-Alive',
    }
    response = requests.get(
        'https://api.linkedin.com/v2/me?projection=(id,profilePicture(displayImage~digitalmediaAsset:playableStreams))',
        headers=headers,
    )
    data = response.json()
    user.profile_image = data.get('profilePicture', {}).get('displayImage~',  {}).get('elements', [{}])[0].get('identifiers', [{}])[0].get('identifier', '')
    user.save()
