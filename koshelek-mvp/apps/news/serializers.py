from rest_framework import serializers
from apps.news.models import News, NewsImage


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsImage
        fields = ('id', 'image', 'news')


class NewsSerializer(serializers.ModelSerializer):
    images = ImageSerializer(read_only=True, many=True)

    class Meta:
        model = News
        fields = ("id", "title", 'description', 'date_added', "images")
        read_only_fields = ('date_added',)
