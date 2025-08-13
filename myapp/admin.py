from django.contrib import admin
from django.utils.html import format_html

from .models import Specialist, CourseCategory, Course

# 👇 Импортируем TranslationAdmin
from modeltranslation.admin import TranslationAdmin


@admin.register(CourseCategory)
class CourseCategoryAdmin(TranslationAdmin):  # Изменили базовый класс
    list_display = ('title',)


@admin.register(Course)
class CourseAdmin(TranslationAdmin):  # Изменили базовый класс
    list_display = ('title', 'category')
    list_filter = ('category',)
    search_fields = ('title', 'short_description')


@admin.register(Specialist)
class SpecialistAdmin(TranslationAdmin):
    list_display = (
        'full_name', 'city', 'specialization',
        'position', 'is_member', 'moderation_status', 'photo_preview'
    )
    search_fields = ('full_name', 'email', 'phone', 'specialization', 'workplace')
    list_filter = ('city', 'is_member', 'category', 'moderation_status')

    def photo_preview(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="width: 40px; height: 40px; object-fit: cover;" />', obj.photo.url)
        return "-"
    photo_preview.short_description = "Фото"
