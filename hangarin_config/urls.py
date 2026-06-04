"""
URL configuration for hangarin_config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib.auth import views as auth_views
from django.http import FileResponse
from django.views.generic import TemplateView
from django.urls import path, re_path, include
from pathlib import Path
from django.conf import settings
from tasks.views import (
    BillingView,
    CategoryListView,
    DashboardView,
    HomeView,
    NoteListView,
    ProfileEditView,
    ProfileView,
    PriorityListView,
    SignUpView,
    SettingsView,
    SocialProfileView,
    SubTaskListView,
    TaskCreateView,
    TaskDeleteView,
    TaskDetailView,
    TaskListView,
    TaskUpdateView,
    mark_task_complete,
)


def service_worker_view(request):
    service_worker_path = Path(settings.BASE_DIR) / 'static' / 'serviceworker.js'
    return FileResponse(service_worker_path.open('rb'), content_type='application/javascript')

urlpatterns = [
    path('debug-urlconf/', TemplateView.as_view(template_name='home.html'), name='debug_urlconf'),
    path('', HomeView.as_view(), name='home'),
    path(
        'manifest.webmanifest',
        TemplateView.as_view(
            template_name='manifest.webmanifest',
            content_type='application/manifest+json',
        ),
        name='manifest',
    ),
    path(
        'serviceworker.js',
        service_worker_view,
        name='serviceworker_compat',
    ),
    path(
        'service-worker.js',
        service_worker_view,
        name='service_worker',
    ),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('tasks/', TaskListView.as_view(), name='tasks'),
    path('subtasks/', SubTaskListView.as_view(), name='subtasks'),
    path('notes/', NoteListView.as_view(), name='notes'),
    path('priorities/', PriorityListView.as_view(), name='priorities'),
    path('categories/', CategoryListView.as_view(), name='categories'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/edit/', ProfileEditView.as_view(), name='profile_edit'),
    path('settings/', SettingsView.as_view(), name='settings'),
    path('social-profile/', SocialProfileView.as_view(), name='social_profile'),
    path('billing/', BillingView.as_view(), name='billing'),
    re_path(r'^tasks/new/?$', TaskCreateView.as_view(), name='task_create'),
    path('tasks/<int:pk>/complete/', mark_task_complete, name='task_complete'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task_detail'),
    path('tasks/<int:pk>/edit/', TaskUpdateView.as_view(), name='task_update'),
    path('tasks/<int:pk>/delete/', TaskDeleteView.as_view(), name='task_delete'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='password_reset_form.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('', include('pwa.urls')), 
]