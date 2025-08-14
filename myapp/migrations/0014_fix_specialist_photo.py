# Создайте новую миграцию командой:
# python manage.py makemigrations myapp --name fix_specialist_photo

# Если миграция не создается автоматически, создайте файл вручную:
# myapp/migrations/0014_fix_specialist_photo.py

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0013_specialist_awards_specialist_email_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='specialist',
            name='photo',
            field=models.ImageField(
                blank=True, 
                help_text='Загрузите фотографию кандидата',
                null=True, 
                upload_to='specialists/photos/', 
                verbose_name='Фотография'
            ),
        ),
    ]