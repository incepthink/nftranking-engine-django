from rest_framework import serializers
from .models import Project


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('name', 'description', 'created_date',
                  'last_refresh', 'ipfs', 'abi', 'address', 'count')


class ProjectMetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('name')
