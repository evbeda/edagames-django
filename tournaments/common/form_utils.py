from tournaments.models import Championship


def get_championships():
    championships = enumerate(Championship.objects.all().values('name'))
    championships_names = [championship[1]['name'] for championship in championships]
    return enumerate(championships_names)
