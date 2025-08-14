from modeltranslation.translator import register, TranslationOptions
from .models import Course, CourseCategory, Specialist

@register(Specialist)
class SpecialistTranslationOptions(TranslationOptions):
    fields = (
        'position', 'about', 'specialization', 'cases', 'category',
        'professional_description', 'skills', 'motivation', 'job_description'
    )
    
@register(CourseCategory)
class CourseCategoryTranslationOptions(TranslationOptions):
    fields = ('title',)

@register(Course)
class CourseTranslationOptions(TranslationOptions):
    fields = ('title', 'short_description', 'full_description',)