from django.urls import path
from .views import signup, HomeView

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('', HomeView.as_view(), name='home'),
]