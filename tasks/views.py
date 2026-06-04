from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView
from django.views.generic import DetailView, UpdateView, DeleteView
from django.views.generic.base import RedirectView
from django.views.decorators.http import require_POST
from tasks.models import Category, Note, Priority, SubTask, Task
from tasks.forms import ProfileForm, SignUpForm, TaskForm

class HomeView(RedirectView):
    pattern_name = 'login'
    permanent = False


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'signup.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Account created successfully. Please log in.')
        return response

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task_qs = Task.objects.select_related('category', 'priority').order_by('deadline')
        counts = task_qs.aggregate(
            pending_count=Count('id', filter=Q(status='Pending')),
            in_progress_count=Count('id', filter=Q(status='In Progress')),
            completed_count=Count('id', filter=Q(status='Completed')),
        )
        context['latest_tasks'] = task_qs.exclude(status='Completed')[:3]
        context['total_tasks'] = task_qs.count()
        context['pending_count'] = counts['pending_count']
        context['in_progress_count'] = counts['in_progress_count']
        context['completed_count'] = counts['completed_count']
        return context

class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks.html'
    paginate_by = 8
    ordering = ('deadline', '-created_at')

    def get_queryset(self):
        return Task.objects.select_related('category', 'priority').order_by(*self.ordering)


class SubTaskListView(LoginRequiredMixin, ListView):
    model = SubTask
    template_name = 'subtasks.html'
    context_object_name = 'subtasks'
    paginate_by = 12

    def get_queryset(self):
        return SubTask.objects.select_related('parent_task').order_by('-created_at')


class NoteListView(LoginRequiredMixin, ListView):
    model = Note
    template_name = 'notes.html'
    context_object_name = 'notes'
    paginate_by = 12

    def get_queryset(self):
        return Note.objects.select_related('task').order_by('-created_at')


class PriorityListView(LoginRequiredMixin, ListView):
    model = Priority
    template_name = 'priorities.html'
    context_object_name = 'priorities'

    def get_queryset(self):
        return Priority.objects.annotate(task_count=Count('task')).order_by('name')


class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'categories.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return Category.objects.annotate(task_count=Count('task')).order_by('name')


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile_form'] = ProfileForm(instance=self.request.user)
        return context


class ProfileEditView(LoginRequiredMixin, UpdateView):
    form_class = ProfileForm
    template_name = 'profile_edit.html'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        return self.request.user


class SettingsView(LoginRequiredMixin, TemplateView):
    template_name = 'settings.html'


class SocialProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'social_profile.html'


class BillingView(LoginRequiredMixin, TemplateView):
    template_name = 'billing.html'


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'task_create.html'
    success_url = reverse_lazy('tasks')

class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'task_detail.html'
    context_object_name = 'task'

    def get_queryset(self):
        return Task.objects.select_related('category', 'priority')

class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'task_update.html'
    success_url = reverse_lazy('tasks')

    def get_queryset(self):
        return Task.objects.select_related('category', 'priority')

class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'task_delete.html'
    success_url = reverse_lazy('tasks')

    def get_queryset(self):
        return Task.objects.select_related('category', 'priority')

class MyProtectedView(LoginRequiredMixin, TemplateView):
    template_name = 'something.html'
    # ... other attributes


@login_required
@require_POST
def mark_task_complete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.status = 'Completed'
    task.save(update_fields=['status', 'updated_at'])
    return redirect('tasks')