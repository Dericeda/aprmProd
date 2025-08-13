from django.db import models

class News(models.Model):
    CATEGORY_CHOICES = [
        ('courses', 'Курсы и вебинары'),
        ('video', 'Видео с YouTube'),
        ('event', 'События'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(verbose_name="Краткое описание")
    full_text = models.TextField(verbose_name="Полное описание", blank=True, null=True)
    image = models.ImageField(upload_to='news_images/', blank=True, null=True)  # обложка
    youtube_url = models.URLField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    views = models.PositiveIntegerField(default=0)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='event')

    def __str__(self):
        return self.title

    @property
    def has_slider(self):
        return self.images.exists()


class NewsImage(models.Model):
    news = models.ForeignKey(
        News,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name="Новость"
    )
    image = models.ImageField("Изображение", upload_to='news/slider/')
    caption = models.CharField("Подпись", max_length=255, blank=True)
    position = models.PositiveIntegerField("Порядок", default=0, help_text="Меньше — раньше в слайдере")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['position', 'id']
        verbose_name = "Фото новости"
        verbose_name_plural = "Фото новости"

    def __str__(self):
        return f"{self.news.title}: {self.caption or self.image.name}"
