from django.shortcuts import render
from rest_framework import viewsets

from fridaygame import models as fg_models
from fridaygame import serializers as fg_serializers


class UserViewSet(viewsets.ModelViewSet):
    queryset = fg_models.User.active_users.all()
    serializer_class = fg_serializers.UserSerializer


class GameViewSet(viewsets.ModelViewSet):
    queryset = fg_models.Game.objects.all()
    serializer_class = fg_serializers.GameSerializer


class TeamViewSet(viewsets.ModelViewSet):
    queryset = fg_models.Team.objects.all()
    serializer_class = fg_serializers.TeamSerializer


class VoteViewSet(viewsets.ModelViewSet):
    queryset = fg_models.Vote.objects.all()
    serializer_class = fg_serializers.VoteSerializer

