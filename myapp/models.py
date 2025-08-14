# myapp/models.py
from django.db import models
from django.utils.text import slugify

class Specialist(models.Model):
    # Личные данные
    full_name = models.CharField("ФИО", max_length=255)
    email = models.EmailField("Электронная почта", blank=True, null=True)
    phone = models.CharField("Телефон", max_length=50, blank=True)
    additional_phone = models.CharField("Дополнительный телефон", max_length=50, blank=True)
    birth_date = models.DateField("Дата рождения", blank=True, null=True)
    citizenship = models.CharField("Гражданство", max_length=100, blank=True)
    city = models.CharField("Город", max_length=100, blank=True)
    social_links = models.TextField("Социальные сети", blank=True)
    
    # Образование
    university = models.CharField("Учебное заведение", max_length=255, blank=True)
    faculty = models.CharField("Факультет/Специальность", max_length=255, blank=True)
    study_years = models.CharField("Годы обучения", max_length=50, blank=True)
    degree = models.CharField("Академическая степень", max_length=100, blank=True)
    
    # Профессиональная деятельность
    position = models.CharField("Должность", max_length=255, blank=True)
    workplace = models.CharField("Место работы", max_length=255, blank=True)
    job_region = models.CharField("Регион работы", max_length=255, blank=True)
    job_description = models.TextField("О компании", blank=True)
    experience_years = models.PositiveIntegerField("Стаж в PR/медиа", default=0, blank=True)
    professional_description = models.TextField("Описание профессиональной деятельности", blank=True)
    
    # Достижения
    skills = models.TextField("Навыки и сертификаты", blank=True)
    awards = models.TextField("Награды", blank=True)
    publications = models.TextField("Публикации", blank=True)
    
    # Мотивация
    motivation = models.TextField("Мотивация", blank=True)
    interests = models.TextField("Интересы", blank=True)  # Будет хранить выбранные чекбоксы как строку
    recommender = models.TextField("Рекомендатель", blank=True)
    
    # Остальные поля
    specialization = models.CharField("Специализация", max_length=255, blank=True)
    about = models.TextField("О себе", blank=True)
    cases = models.TextField("Кейсы", blank=True)
    is_member = models.BooleanField("Участник Ассоциации", default=False)
    category = models.CharField("Категория", max_length=100, blank=True)
    
    # Файлы
    photo = models.ImageField("Фотография", upload_to="specialists/photos/", blank=True, null=True)
    resume = models.FileField("Резюме/CV", upload_to="specialists/resumes/", blank=True, null=True)
    documents = models.FileField("Дополнительные документы", upload_to="specialists/documents/", blank=True, null=True)
    
    # Статус и даты
    moderation_status = models.CharField("Статус модерации", max_length=50, choices=[
        ('pending', 'На модерации'),
        ('approved', 'Одобрен'),
        ('rejected', 'Отклонён'),
    ], default='pending')
    created_at = models.DateTimeField("Дата подачи заявки", auto_now_add=True)
    updated_at = models.DateTimeField("Дата обновления", auto_now=True)
    
    # Согласия
    confirm_data = models.BooleanField("Подтверждение достоверности данных", default=False)
    consent_personal_data = models.BooleanField("Согласие на обработку персональных данных", default=False)

    def __str__(self):
        return f"{self.full_name} ({self.city})"
    
    class Meta:
        verbose_name = "Специалист"
        verbose_name_plural = "Специалисты"
        ordering = ['-created_at']

class CourseCategory(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while CourseCategory.objects.filter(slug=slug).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Course(models.Model):
    category = models.ForeignKey(CourseCategory, on_delete=models.CASCADE, related_name='courses')
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='courses/')
    short_description = models.TextField()
    full_description = models.TextField()
    youtube_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title