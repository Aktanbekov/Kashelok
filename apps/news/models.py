from django.db import models


class News(models.Model):
    title = models.CharField(verbose_name='title', max_length=70, blank=True, null=True)
    description = models.TextField(verbose_name='description', blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title}'


class NewsImage(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(verbose_name='image')

    def __str__(self):
        return f'{self.news.title}'
