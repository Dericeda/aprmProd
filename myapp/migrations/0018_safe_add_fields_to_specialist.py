# myapp/migrations/0018_safe_add_fields_to_specialist.py
# Создайте этот файл вручную

from django.db import migrations, models
from django.db import connection


def field_exists(table_name, field_name):
    """Проверяет, существует ли поле в таблице"""
    cursor = connection.cursor()
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [column[1] for column in cursor.fetchall()]
    return field_name in columns


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0017_merge_20250814_0413'),  # замените на вашу последнюю миграцию
    ]

    operations = []

    def __init__(self, name, app_label):
        super().__init__(name, app_label)
        
        # Список полей для добавления
        fields_to_add = [
            ('additional_phone', models.CharField(blank=True, max_length=50, verbose_name='Дополнительный телефон')),
            ('citizenship', models.CharField(blank=True, max_length=100, verbose_name='Гражданство')),
            ('university', models.CharField(blank=True, max_length=255, verbose_name='Учебное заведение')),
            ('faculty', models.CharField(blank=True, max_length=255, verbose_name='Факультет/Специальность')),
            ('study_years', models.CharField(blank=True, max_length=50, verbose_name='Годы обучения')),
            ('professional_description', models.TextField(blank=True, verbose_name='Описание профессиональной деятельности')),
            ('interests', models.TextField(blank=True, verbose_name='Интересы')),
            ('resume', models.FileField(blank=True, null=True, upload_to='specialists/resumes/', verbose_name='Резюме/CV')),
            ('documents', models.FileField(blank=True, null=True, upload_to='specialists/documents/', verbose_name='Дополнительные документы')),
            ('confirm_data', models.BooleanField(default=False, verbose_name='Подтверждение достоверности данных')),
            ('consent_personal_data', models.BooleanField(default=False, verbose_name='Согласие на обработку персональных данных')),
            ('consent_rules', models.BooleanField(default=False, verbose_name='Согласие с правилами Ассоциации')),
        ]
        
        # Добавляем операции только для полей, которых нет
        for field_name, field in fields_to_add:
            if not field_exists('myapp_specialist', field_name):
                self.operations.append(
                    migrations.AddField(
                        model_name='specialist',
                        name=field_name,
                        field=field,
                    )
                )
        
        # Добавляем временные поля отдельно, так как они требуют preserve_default=False
        timestamp_fields = [
            ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата подачи заявки')),
            ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
        ]
        
        for field_name, field in timestamp_fields:
            if not field_exists('myapp_specialist', field_name):
                self.operations.append(
                    migrations.AddField(
                        model_name='specialist',
                        name=field_name,
                        field=field,
                        preserve_default=False,
                    )
                )