# Создайте новую миграцию командой:
# python manage.py makemigrations myapp

# Или создайте файл myapp/migrations/0002_update_specialist_model.py

from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),  # замените на актуальную последнюю миграцию
    ]
    
    operations = [
        # Добавляем новые поля
        migrations.AddField(
            model_name='specialist',
            name='additional_phone',
            field=models.CharField(blank=True, max_length=50, verbose_name='Дополнительный телефон'),
        ),
        migrations.AddField(
            model_name='specialist',
            name='birth_date',
            field=models.DateField(blank=True, null=True, verbose_name='Дата рождения'),
        ),
        migrations.AddField(
            model_name='specialist',
            name='citizenship',
            field=models.CharField(blank=True, max_length=100, verbose_name='Гражданство'),
        ),
        migrations.AddField(
            model_name='specialist',
            name='university',
            field=models.CharField(blank=True, max_length=255, verbose_name='Учебное заведение'),
        ),
        migrations.AddField(
            model_name='specialist',
            name='faculty',
            field=models.CharField(blank=True, max_length=255, verbose_name='Факультет/Специальность'),
        ),
        migrations.AddField(
            model_name='specialist',
            name='study_years',
            field=models.CharField(blank=True, max_length=50, verbose_name='Годы обучения'),
        ),
        migrations.AddField(
            model_name='specialist',
            name='degree',
            field=models.CharField(blank=True, max_length=100, verbose_name='Академическая степень'),
        ),
        migrations.AddField(
            model_name='specialist',
            name='professional_description',
            field=models.TextField(blank=True, verbose_name='Описание профессиональной деятельности'),
        ),
        migrations.AddField(
            model_name='specialist',
            name='interests',
            field=models.TextField(blank=True, verbose_name='Интересы'),
        ),
        migrations.AddField(
            model_name='specialist',
            name='resume',
            field=models.FileField(blank=True, null=True, upload_to='specialists/resumes/', verbose_name='Резюме/CV'),
        ),
        migrations.AddField(
            model_name='specialist',
            name='documents',
            field=models.FileField(blank=True, null=True, upload_to='specialists/documents/', verbose_name='Дополнительные документы'),
        ),
        migrations.AddField(
            model_name='specialist',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата подачи заявки'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='specialist',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата обновления'),
        ),
        migrations.AddField(
            model_name='specialist',
            name='confirm_data',
            field=models.BooleanField(default=False, verbose_name='Подтверждение достоверности данных'),
        ),
        migrations.AddField(
            model_name='specialist',
            name='consent_personal_data',
            field=models.BooleanField(default=False, verbose_name='Согласие на обработку персональных данных'),
        ),
        
        # Обновляем существующие поля
        migrations.AlterField(
            model_name='specialist',
            name='social_links',
            field=models.TextField(blank=True, verbose_name='Социальные сети'),
        ),
    ]