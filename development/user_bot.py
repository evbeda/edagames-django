from social_django.storage import DjangoUserMixin


@classmethod
def create_user(cls, username, email=None):
    """Create a user with given username and (optional) email"""
    raise NotImplementedError('Implement in subclass')