from rest_framework import serializers

from .models import Project


class ProjectSerializer(serializers.ModelSerializer):
    """ Project Serializer """

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'created_at', 'updated_at']