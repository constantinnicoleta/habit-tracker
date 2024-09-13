from django.contrib import admin
from .models import Habit, Progress

# Register models
admin.site.register(Habit)
admin.site.register(Progress)
