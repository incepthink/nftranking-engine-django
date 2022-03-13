from rest_framework import serializers
from .models import Project


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('name', 'description', 'created_date',
                  'last_refresh', 'ipfs', 'abi', 'address', 'count', 'banner_link', 'total_supply', 'volume')


class ProjectMetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('name')
