from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from .models import News, NewsImage  # ⬅️ добавили NewsImage

class NewsImageInline(admin.TabularInline):
    model = NewsImage
    fields = ("image", "caption", "position")
    extra = 1
    ordering = ("position",)

@admin.register(News)
class NewsAdmin(TranslationAdmin):
    list_display = ("title", "date", "category")
    search_fields = ("title", "description")
    list_filter = ("category", "date")
    inlines = [NewsImageInline]  # ⬅️ добавили инлайн

# (опционально) отдельная админ-страница для картинок
@admin.register(NewsImage)
class NewsImageAdmin(admin.ModelAdmin):
    list_display = ("id", "news", "position", "caption", "created_at")
    list_filter = ("news",)
    ordering = ("news", "position", "id")
