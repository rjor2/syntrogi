from rest_framework import serializers
from .models import Repo

class RepoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Repo
        fields = ('id', 'name', 'url', 'branch', 'revision', 'downloaded')


