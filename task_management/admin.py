from django.contrib import admin

from .models import Task


# admin.site.register(Post)
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'description', 'completed', 'created_at', 'user']
