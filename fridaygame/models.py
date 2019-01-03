from django.db import models


class Base(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ActiveUsers(models.QuerySet):
    def users(self):
        return self.filter(is_active=True)


class User(Base):
    first_name = models.CharField(max_length=40, null=True)
    last_name = models.CharField(max_length=40, blank=True, null=True)
    username = models.CharField(max_length=40, unique=True)
    is_active = models.BooleanField(default=True)
    token = models.CharField(max_length=200, null=True, blank=True)

    objects = models.Manager()
    active_users = ActiveUsers.as_manager()

    def __str__(self):
        if self.first_name:
            if self.last_name:
                return "{} {}".format(self.first_name, self.last_name)
            else:
                return "{}".format(self.first_name)
        else:
            return self.username


class Game(Base):
    name = models.CharField(max_length=40)
    description = models.TextField(blank=True, null=True)
    max_team_size = models.PositiveSmallIntegerField()
    min_team_size = models.PositiveSmallIntegerField()
    max_teams = models.PositiveIntegerField()
    min_teams = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class Team(Base):
    TEAM_NAMES = (
        ('R', 'RED'),
        ('Y', 'YELLOW'),
        ('G', 'GREEN'),
        ('B', 'BLUE'),
        ('P', 'PURPLE'),
        ('O', 'ORANGE')
    )
    users = models.ManyToManyField(User, related_name="my_teams")
    game_for_team = models.ForeignKey(
                Game,
                on_delete=models.SET_NULL,
                null=True,
                related_name="game_teams"
            )
    name = models.CharField(
                    choices=TEAM_NAMES, max_length=1,
                    blank=True, null=True
                )

    def __str__(self):
        return self.name


class Vote(Base):
    voted_user = models.ForeignKey(
                    User,
                    on_delete=models.SET_NULL, null=True,
                    related_name="my_votes",
                    db_index=False
                    # limit_choices_to={"is_active":True}
                )
    game_chosen = models.ForeignKey(
                    Game,
                    on_delete=models.SET_NULL,
                    null=True,
                    related_name="votes",
                    db_index=False
                )
    date = models.DateField(null=True)
    voted = models.BooleanField(default=False)

    def __str__(self):
        return '{}-{}-{}'.format(self.voted_user, self.game_chosen, self.date)

    class Meta:
        unique_together = ('date', 'voted_user', 'game_chosen')

