from django.urls import path
from .views import signup, HomeView, dashboard, add_habit, edit_habit, delete_habit, track_progress, todays_habits, finish_habit

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('', HomeView.as_view(), name='home'),
    path('todays-habits/', todays_habits, name='todays_habits'),
    path('dashboard/', dashboard, name='dashboard'),
    path('add-habit/', add_habit, name='add_habit'),
    path('edit-habit/<int:habit_id>/', edit_habit, name='edit_habit'),
    path('delete-habit/<int:habit_id>/', delete_habit, name='delete_habit'),
    path('track-progress/<int:habit_id>/', track_progress, name='track_progress'),
    path('finish-habit/<int:habit_id>/', finish_habit, name='finish_habit'),
]