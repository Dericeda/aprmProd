# translation.py

from modeltranslation.translator import register, TranslationOptions
from .models import Course, CourseCategory
from .models import Course, CourseCategory, Specialist  # 👈 добавили Specialist

@register(Specialist)
class SpecialistTranslationOptions(TranslationOptions):
    fields = ('position', 'about', 'specialization', 'cases', 'category',)
    
@register(CourseCategory)
class CourseCategoryTranslationOptions(TranslationOptions):
    fields = ('title',)

@register(Course)
class CourseTranslationOptions(TranslationOptions):
    fields = ('title', 'short_description', 'full_description',)
