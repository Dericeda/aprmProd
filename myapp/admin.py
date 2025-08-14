# myapp/admin.py
from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from .models import Specialist, CourseCategory, Course

# Импортируем TranslationAdmin
from modeltranslation.admin import TranslationAdmin


@admin.register(CourseCategory)
class CourseCategoryAdmin(TranslationAdmin):
    list_display = ('title',)


@admin.register(Course)
class CourseAdmin(TranslationAdmin):
    list_display = ('title', 'category')
    list_filter = ('category',)
    search_fields = ('title', 'short_description')


@admin.register(Specialist)
class SpecialistAdmin(TranslationAdmin):
    list_display = (
        'full_name', 
        'city', 
        'specialization',
        'position', 
        'is_member', 
        'moderation_status', 
        'photo_preview'
    )
    list_display_links = ('full_name',)
    search_fields = ('full_name', 'email', 'phone', 'specialization', 'workplace')
    list_filter = ('city', 'is_member', 'category', 'moderation_status')
    list_editable = ('moderation_status', 'is_member')
    
    # Группировка полей в админке
    fieldsets = (
        ('Основная информация', {
            'fields': ('full_name', 'email', 'phone', 'photo')
        }),
        ('Профессиональная информация', {
            'fields': ('position', 'workplace', 'city', 'specialization', 'category')
        }),
        ('Подробности', {
            'fields': ('about', 'job_description', 'experience_years')
        }),
        ('Достижения', {
            'fields': ('skills', 'awards', 'publications', 'cases')
        }),
        ('Модерация', {
            'fields': ('moderation_status', 'is_member')
        }),
        ('Дополнительно', {
            'fields': ('social_links', 'motivation', 'recommender'),
            'classes': ('collapse',)
        }),
    )

    def photo_preview(self, obj):
        """Метод для отображения превью фото в списке"""
        if obj.photo:
            try:
                return format_html(
                    '<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 50%;" />',
                    obj.photo.url
                )
            except Exception as e:
                return format_html(
                    '<span style="color: red;">Ошибка загрузки: {}</span>',
                    str(e)
                )
        return format_html('<span style="color: gray;">Нет фото</span>')
    
    photo_preview.short_description = "Фото"
    photo_preview.allow_tags = True

    def get_readonly_fields(self, request, obj=None):
        """Делаем некоторые поля только для чтения"""
        readonly_fields = []
        if obj:  # если редактируем существующий объект
            readonly_fields = ['email', 'phone']
        return readonly_fields

    # Добавляем actions для массовых операций
    actions = ['approve_specialists', 'reject_specialists', 'make_members']

    def approve_specialists(self, request, queryset):
        """Одобрить выбранных специалистов"""
        updated = queryset.update(moderation_status='approved')
        self.message_user(request, f'Одобрено {updated} специалистов.')
    approve_specialists.short_description = "Одобрить выбранных специалистов"

    def reject_specialists(self, request, queryset):
        """Отклонить выбранных специалистов"""
        updated = queryset.update(moderation_status='rejected')
        self.message_user(request, f'Отклонено {updated} специалистов.')
    reject_specialists.short_description = "Отклонить выбранных специалистов"

    def make_members(self, request, queryset):
        """Сделать участниками ассоциации"""
        updated = queryset.update(is_member=True)
        self.message_user(request, f'{updated} специалистов стали участниками ассоциации.')
    make_members.short_description = "Сделать участниками ассоциации"

    def export_excel(self, request):
        # Создаем Excel файл
        workbook = openpyxl.Workbook()
        worksheet = workbook.active
        worksheet.title = "Заявки специалистов"

        # Заголовки
        headers = [
            'ФИО', 'Email', 'Телефон', 'Доп. телефон', 'Дата рождения', 'Гражданство',
            'Город', 'Соцсети', 'Учебное заведение', 'Факультет', 'Годы обучения',
            'Академическая степень', 'Должность', 'Место работы', 'Регион работы',
            'Описание компании', 'Стаж (лет)', 'Описание деятельности', 'Навыки',
            'Награды', 'Публикации', 'Мотивация', 'Интересы', 'Рекомендатель',
            'Специализация', 'Категория', 'Участник ассоциации', 'Статус модерации',
            'Дата подачи заявки', 'Подтверждение данных', 'Согласие на обработку'
        ]

        # Записываем заголовки
        for col, header in enumerate(headers, 1):
            cell = worksheet.cell(row=1, column=col, value=header)
            cell.font = Font(bold=True)
            cell.alignment = Alignment(horizontal='center')

        # Получаем данные
        specialists = Specialist.objects.all().order_by('-created_at')

        # Записываем данные
        for row, specialist in enumerate(specialists, 2):
            data = [
                specialist.full_name,
                specialist.email,
                specialist.phone,
                specialist.additional_phone,
                specialist.birth_date.strftime('%d.%m.%Y') if specialist.birth_date else '',
                specialist.citizenship,
                specialist.city,
                specialist.social_links,
                specialist.university,
                specialist.faculty,
                specialist.study_years,
                specialist.degree,
                specialist.position,
                specialist.workplace,
                specialist.job_region,
                specialist.job_description,
                specialist.experience_years,
                specialist.professional_description,
                specialist.skills,
                specialist.awards,
                specialist.publications,
                specialist.motivation,
                specialist.interests,
                specialist.recommender,
                specialist.specialization,
                specialist.category,
                'Да' if specialist.is_member else 'Нет',
                specialist.get_moderation_status_display(),
                specialist.created_at.strftime('%d.%m.%Y %H:%M'),
                'Да' if specialist.confirm_data else 'Нет',
                'Да' if specialist.consent_personal_data else 'Нет',
            ]
            
            for col, value in enumerate(data, 1):
                worksheet.cell(row=row, column=col, value=value)

        # Автоширина колонок
        for column in worksheet.columns:
            max_length = 0
            column_letter = column[0].column_letter
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = min(max_length + 2, 50)
            worksheet.column_dimensions[column_letter].width = adjusted_width

        # Создаем HTTP ответ
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        filename = f"specialists_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        
        workbook.save(response)
        return response

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['export_url'] = reverse('admin:specialist_export_excel')
        return super().changelist_view(request, extra_context)