from django.urls import path

from apps.news.views import ImageView, NewsView, NewsPhotoView

urlpatterns = [
    path("news/", NewsView.as_view(), name='news'),
    path('news_photo/', ImageView.as_view(), name='photo'),
    path('news_view/', NewsPhotoView.as_view(), name='news_view')
]
