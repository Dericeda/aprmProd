from django.db import models
from django.contrib.auth.models import User

class AssociationMember(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=1)
    patronymic = models.CharField(max_length=100, default='—')
    workplace = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    contacts = models.TextField()
    motivation_letter = models.TextField()
    social_networks = models.CharField(max_length=255, blank=False, default='No social networks')
    resume = models.FileField(upload_to='resumes/')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.get_full_name()}"