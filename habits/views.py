from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from .forms import CustomUserCreationForm
from .models import Habit
from .forms import HabitForm
from .models import Progress

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


@login_required
def add_habit(request):
    if request.method == 'POST':
        form = HabitForm(request.POST)
        if form.is_valid():
            habit = form.save(commit=False)
            habit.user = request.user
            habit.save()
            return redirect('dashboard')
    else:
        form = HabitForm()

    return render(request, 'add_habit.html', {'form': form})    


# View the user's dashboard with all their habits
 # Render the dashboard with the user's habits
@login_required
def dashboard(request):
    user_habits = Habit.objects.filter(user=request.user)
    return render(request, 'dashboard.html', {'user_habits': user_habits})


# Edit an existing habit
# Get the habit that matches the habit_id and belongs to the logged-in user
@login_required
def edit_habit(request, habit_id):
    habit = Habit.objects.get(id=habit_id, user=request.user)
    
    if request.method == 'POST':
        form = HabitForm(request.POST, instance=habit)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = HabitForm(instance=habit)
    
    return render(request, 'edit_habit.html', {'form': form})


# Edit an existing habit
@login_required
def delete_habit(request, habit_id):
    habit = Habit.objects.get(id=habit_id, user=request.user)
    
    if request.method == 'POST':
        habit.delete()
        return redirect('dashboard')
    
    return render(request, 'delete_habit.html', {'habit': habit})

# Track progress for a specific habit
@login_required
def track_progress(request, habit_id):
    habit = get_object_or_404(Habit, id=habit_id, user=request.user)
    today = timezone.now().date()

    # Get or create progress for today's date
    progress, created = Progress.objects.get_or_create(
        habit=habit, date=today, defaults={'completed': False}
    )

    # Handle form submission (when user marks progress as completed)
    if request.method == 'POST':
        progress.completed = True
        progress.save()
        return redirect('dashboard')

    # Fetch all progress entries for this habit to display history
    progress_history = Progress.objects.filter(habit=habit).order_by('-date')

    return render(request, 'track_progress.html', {
        'habit': habit,
        'today': today,
        'progress': progress,
        'progress_history': progress_history
    })
