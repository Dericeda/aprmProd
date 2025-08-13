from django.contrib import admin
from .models import AssociationMember

@admin.register(AssociationMember)
class AssociationMemberAdmin(admin.ModelAdmin):
    list_display = ('user', 'workplace', 'position')