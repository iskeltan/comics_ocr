from rest_framework import serializers

from comics.models import Comic


class ComicSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comic
        fields = ("id", "image")