from django.contrib import admin

# Register your models here.
from teacherapp.models import Subject, Teacher


class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'color']
    list_display_links = ['name']

admin.site.register(Subject, SubjectAdmin)

admin.site.register(Teacher)
