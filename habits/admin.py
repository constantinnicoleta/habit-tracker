from django.contrib import admin
from .models import Habit, Progress

# Register your models here.
admin.site.register(Habit)
admin.site.register(Progress)
