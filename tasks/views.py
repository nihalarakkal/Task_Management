from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Task, User
from .forms import TaskForm, CompletionForm, UserForm

# ----------------------
# Role check decorators
# ----------------------
def is_superadmin(user):
    return user.role == 'superadmin'

def is_admin(user):
    return user.role == 'admin'

def is_user(user):
    return user.role == 'user'


# ----------------------
# Authentication
# ----------------------
def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            if user.role == 'superadmin':
                return redirect('superadmin_dashboard')
            elif user.role == 'admin':
                return redirect('admin_dashboard')
            else:
                return redirect('user_dashboard')
        else:
            messages.error(request, "Invalid credentials")
    return render(request, 'tasks/login.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


# ----------------------
# Dashboards
# ----------------------
@login_required
@user_passes_test(is_superadmin)
def superadmin_dashboard(request):
    users = User.objects.all()
    tasks = Task.objects.all()
    return render(request, 'tasks/superadmin_dashboard.html', {'users': users, 'tasks': tasks})


@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    tasks = Task.objects.filter(assigned_to__role='user')
    users = User.objects.filter(role='user')
    return render(request, 'tasks/admin_dashboard.html', {'tasks': tasks, 'users': users})


@login_required
@user_passes_test(is_user)
def user_dashboard(request):
    tasks = Task.objects.filter(assigned_to=request.user)
    return render(request, 'tasks/user_dashboard.html', {'tasks': tasks})


# ----------------------
# Task Management (Admin)
# ----------------------
@login_required
@user_passes_test(is_admin)
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Task assigned successfully")
            return redirect('admin_dashboard')
    else:
        form = TaskForm()
    return render(request, 'tasks/create_task.html', {'form': form})


@login_required
@user_passes_test(is_user)
def complete_task(request, pk):
    task = get_object_or_404(Task, pk=pk, assigned_to=request.user)
    if request.method == 'POST':
        form = CompletionForm(request.POST, instance=task)
        if form.is_valid():
            task.status = 'completed'
            form.save()  # saves completion_report & worked_hours
            messages.success(request, "Task completed successfully!")
            return redirect('user_dashboard')
    else:
        form = CompletionForm(instance=task)
    return render(request, 'tasks/complete_task.html', {'form': form, 'task': task})

@login_required
def view_report(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.user.role not in ['admin', 'superadmin']:
        messages.error(request, "You do not have access")
        return redirect('login')
    return render(request, 'tasks/task_report.html', {'task': task})


# ----------------------
# Task Management (SuperAdmin)
# ----------------------
@login_required
@user_passes_test(is_superadmin)
def superadmin_tasks(request):
    tasks = Task.objects.all()
    return render(request, 'tasks/superadmin_tasks.html', {'tasks': tasks})


@login_required
@user_passes_test(is_superadmin)
def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Task added successfully")
            return redirect('superadmin_tasks')
    else:
        form = TaskForm()
    return render(request, 'tasks/add_task.html', {'form': form})


@login_required
@user_passes_test(is_superadmin)
def edit_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, "Task updated successfully")
            return redirect('superadmin_tasks')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/edit_task.html', {'form': form, 'task': task})


@login_required
@user_passes_test(is_superadmin)
def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.delete()
    messages.success(request, "Task deleted successfully")
    return redirect('superadmin_tasks')


@login_required
@user_passes_test(is_superadmin)
def view_task_report(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if task.status == 'completed':
        return render(request, 'tasks/view_report.html', {'task': task})
    else:
        messages.error(request, "Task not completed yet")
        return redirect('superadmin_tasks')


# ----------------------
# SuperAdmin: User/Admin Management
# ----------------------
@login_required
@user_passes_test(is_superadmin)
def manage_users(request):
    users = User.objects.all()
    return render(request, 'tasks/manage_users.html', {'users': users})


@login_required
@user_passes_test(is_superadmin)
def add_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "User added successfully")
            return redirect('manage_users')
    else:
        form = UserForm()
    return render(request, 'tasks/add_user.html', {'form': form})


@login_required
@user_passes_test(is_superadmin)
def edit_user(request, pk):
    user_obj = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user_obj.username = request.POST['username']
        user_obj.email = request.POST['email']
        user_obj.role = request.POST['role']
        user_obj.save()
        messages.success(request, "User updated successfully")
        return redirect('superadmin_dashboard')
    return render(request, 'tasks/edit_user.html', {'user': user_obj})


@login_required
@user_passes_test(is_superadmin)
def delete_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    user.delete()
    messages.success(request, "User deleted successfully")
    return redirect('manage_users')


@login_required
@user_passes_test(is_superadmin)
def change_admin_role(request, pk):
    user = get_object_or_404(User, pk=pk)
    if user.role == 'admin':
        user.role = 'superadmin'
        messages.success(request, f"{user.username} promoted to SuperAdmin")
    elif user.role == 'superadmin':
        user.role = 'admin'
        messages.success(request, f"{user.username} demoted to Admin")
    user.save()
    return redirect('superadmin_dashboard')


# Optional: edit_admin (if separate from edit_user)
@login_required
@user_passes_test(is_superadmin)
def edit_admin(request, pk):
    admin_user = get_object_or_404(User, pk=pk, role='admin')
    if request.method == 'POST':
        admin_user.username = request.POST['username']
        admin_user.email = request.POST['email']
        admin_user.role = request.POST['role']
        admin_user.save()
        messages.success(request, "Admin updated successfully")
        return redirect('superadmin_dashboard')
    return render(request, 'tasks/edit_user.html', {'user': admin_user})
@login_required
@user_passes_test(is_admin)
def admin_edit_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, "Task updated successfully")
            return redirect('admin_dashboard')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/admin_edit_task.html', {'form': form, 'task': task})

@login_required
@user_passes_test(is_admin)
def admin_delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.delete()
    messages.success(request, "Task deleted successfully")
    return redirect('admin_dashboard')
from django.contrib import admin
from .models import Task


