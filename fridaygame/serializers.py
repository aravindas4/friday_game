from rest_framework import serializers

from fridaygame import models as fg_models


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = fg_models.User
        fields = '__all__'


class GameSerializer(serializers.ModelSerializer):

    class Meta:
        model = fg_models.Game
        fields = '__all__'


class TeamSerializer(serializers.ModelSerializer):
    users = serializers.StringRelatedField(
        many=True,
        read_only=True,
    )
    game_for_team = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = fg_models.Team
        fields = ('id','users', 'game_for_team', 'name',)


class VoteSerializer(serializers.ModelSerializer):
    voted_user = serializers.StringRelatedField(
        many=True,
        read_only=True,
    )
    game_for_team = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = fg_models.Vote
        fields = ('id','voted_user','game_for_team','date',)

