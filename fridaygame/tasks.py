import random

from celery import task
from django.core.mail import send_mass_mail
from django.conf import settings
from django.db.models import F, Count

from fridaygame.models import models as fg_models


@task(name="polls")
def send_polls_url_email():
    subject = 'Test MAil'
    message = ' Be ready for polls'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['ash.g.proxy@gmail.com']
    return send_mass_mail(subject, message, email_from, recipient_list)


def choose_game(date):
    votes_list_count = fg_models.Vote.objects.filter(date=date, voted=True)
    games_list = fg_models.Game.objects.all()
    filtered_games = games_list\
                        .annotate(min_people=F('min_team_size') * F('min_teams'))\
                        .filter(min_people_lte=votes_list_count)

    voted_games = games_list\
                        .filter(votes__date=date)\
                        .annotate(voted_games=Count('votes'))\
                        .values('id', 'name', 'total_votes').order_by('-total_votes')

    max_voted_games = voted_games.filter(voted_games=Max('voted_games'))

    final_games_list = filtered_games().filter(id__in=max_voted_games.values('id'))

    if final_games_list.exists():
        if final_games_list.count() == 1:
            return final_games_list.first(), votes_list_count
        else:
            return random.choice(final_games_list), votes_list_count
    else:
        return None, votes_list_count


def choose_teams(game, count, date):
    users_count = count
    if game.name.lower() = "pictionary":
        teams = game.min_teams
        team_size = game.min_team_size
        count = count - (teams * team_size)

        while (team_size <= game.max_team_size) and (count>0):
            team_size += 1
            count -= teams

    elif game.name.lower() == "taboo":
        teams = game.min_teams
        team_size = count / teams
    else:
        teams = count
        team_size = game.min_team_size

    users_list = list(fg_models.User.objects.filter(my_votes__date=date).values_list('id', flat=True))

    team_names = list(fg_models.TEAM_NAMES)

    final_teams = []
    final_team_names = []
    for i in range(teams):
        current_team = []
        for j in range(team_size):
            if users_list:
                user = random.choice(users_list)
                current_team.append(user)
                users_list.remove(user)
        tname = random.choice(team_names)
        final_team_names.append(tname)
        final_teams.append(current_team)

    return final_teams, final_team_names

@task(name="calculate_results")
def compute_results(date):
    game, count = choose_game(date)
    if game:
        teams = choose_teams(game, count, date)

@task(name="results")
def send_polls_results_email():
    subject = 'Test MAil'
    message = ' Be ready for polls'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['ash.g.proxy@gmail.com']
    return send_mass_mail(subject, message, email_from, recipient_list)
