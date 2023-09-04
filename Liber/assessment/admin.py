from django.contrib import admin
from .models import Assessment, Question, Section
# Register your models here.

admin.site.register(Assessment)
admin.site.register(Question)
admin.site.register(Section)