from django.db import models
from django.contrib.auth.models import User

# Create your models here.

#Habit Model represents a habit that a user wants to track.
#Linked to the User model via a ForeignKey
class Habit(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    start_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


# The Progress model tracks whether a habit was completed on a specific date.
# Linked to the Habit model via a ForeignKey.
class Progress(models.Model):
    id = models.AutoField(primary_key=True)
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.habit.name} - {self.date}"        

