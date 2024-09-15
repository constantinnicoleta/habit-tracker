from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
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

    template_name = 'habits/home.html'

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
    return render(request, 'habits/signup.html', {'form': form})


@login_required
def add_habit(request):
    if request.method == 'POST':
        form = HabitForm(request.POST)
        if form.is_valid():
            habit = form.save(commit=False)
            habit.user = request.user
            habit.save()
            messages.success(
                request,
                f'Your new habit "{habit.name}" was successfully added.')
            return redirect('dashboard')
    else:
        form = HabitForm()

    return render(request, 'habits/add_habit.html', {'form': form})


# View the user's dashboard with all their habits
# Render the dashboard with the user's habits
@login_required
def dashboard(request):
    # Get the filter type from the query parameters (default to 'all')
    filter_type = request.GET.get('filter', 'all')

    if filter_type == 'finished':
        # Filter habits that are marked as finished
        user_habits = Habit.objects.filter(user=request.user, finished=True)
    elif filter_type == 'unfinished':
        # Filter habits that are not marked as finished
        user_habits = Habit.objects.filter(user=request.user, finished=False)
    else:
        # Default: Get all habits for the logged-in user
        user_habits = Habit.objects.filter(user=request.user)

    return render(request, 'habits/dashboard.html',
                  {'user_habits': user_habits, 'filter_type': filter_type})


# Edit an existing habit
# Get the habit that matches the habit_id and belongs to the logged-in user
@login_required
def edit_habit(request, habit_id):
    habit = Habit.objects.get(id=habit_id, user=request.user)

    if request.method == 'POST':
        form = HabitForm(request.POST, instance=habit)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your habit "{habit.name}" was successfully updated.')
            return redirect('dashboard')
    else:
        form = HabitForm(instance=habit)

    return render(request, 'habits/edit_habit.html', {'form': form})


# Edit an existing habit
@login_required
def delete_habit(request, habit_id):
    habit = Habit.objects.get(id=habit_id, user=request.user)

    if request.method == 'POST':
        habit.delete()
        messages.success(request, f'Your habit "{habit.name}" was successfully deleted.')
        return redirect('dashboard')

    return render(request, 'habits/delete_habit.html', {'habit': habit})


# Track progress for a specific habit
@login_required
def track_progress(request, habit_id):
    # Get today's date
    today = timezone.now().date()

    # Get the 'from' parameter to determine the origin of the request
    from_page = request.GET.get('from', 'dashboard')

    # Get the habit and create a new Progress entry
    habit = Habit.objects.get(id=habit_id, user=request.user)
    progress, created = Progress.objects.get_or_create(habit=habit, date=today)

    if request.method == 'POST':
        # Mark the habit as completed for today
        progress.completed = True
        progress.save()

        # Check if there are still unmarked habits for today
        unmarked_habits = Habit.objects.filter(user=request.user).exclude(
            progress__date=today, progress__completed=True
        )

        return redirect('todays_habits')

    # If GET request, show the tracking form
    progress_history = Progress.objects.filter(habit=habit).order_by('-date')

    context = {
        'habit': habit,
        'today': today,
        'progress': progress,
        'progress_history': progress_history,
        'from_page': from_page,
    }

    return render(request, 'habits/track_progress.html', context)


@login_required
def todays_habits(request):
    # Get today's date
    today = timezone.now().date()

    # Get user's habits that are not marked as completed today
    unmarked_habits = Habit.objects.filter(user=request.user).exclude(
        progress__date=today, progress__completed=True
    )

    context = {
        'unmarked_habits': unmarked_habits,
        'today': today
    }

    return render(request, 'habits/todays_habits.html', context)


# View to mark habit as finished
@login_required
def finish_habit(request, habit_id):
    habit = get_object_or_404(Habit, id=habit_id, user=request.user)
    habit.finished = True
    habit.save()
    return redirect('dashboard')
    