from tournaments.models import Championship, Tournament

def get_championships():
    championships = enumerate(Championship.objects.all().values('name'))
    championships_names = [championship[1]['name'] for championship in championships]
    return enumerate(championships_names)

def get_tournaments_associated_with_championship():
    tournaments = enumerate(Tournament.objects.exclude(championship=None).values('name'))
    tournaments_name = [tournament[1]['name'] for tournament in tournaments]
    return enumerate(tournaments_name)