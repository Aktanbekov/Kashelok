from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import AllowAny
from apps.news.models import News, NewsImage
from apps.news.serializers import NewsSerializer, ImageSerializer


class ImageView(CreateAPIView):
    queryset = NewsImage.objects.all()
    serializer_class = ImageSerializer


class NewsView(CreateAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = (AllowAny,)


class NewsPhotoView(ListAPIView):
    queryset = (News.objects.all())
    serializer_class = NewsSerializer
    permission_classes = (AllowAny,)
