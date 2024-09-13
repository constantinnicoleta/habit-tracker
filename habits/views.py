from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.views.generic import TemplateView
from .forms import CustomUserCreationForm 

# HomeView renders the 'home.html' template when accessed
class HomeView(TemplateView):
    template_name = 'home.html'


# Handle form submission (POST request)
# Get data from the form & validate 
# Create, save & redirect user to the home page after sign-up
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  
            return redirect('home')  
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})