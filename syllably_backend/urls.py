from django.contrib.auth import views as auth_views
from django.http import FileResponse
from django.views.generic import TemplateView
from django.contrib import admin
from django.urls import path, re_path, include
from pathlib import Path
from django.conf import settings

# Import your views
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
    path('admin/', admin.site.urls),
    
    # Core Application Routes
    path('', HomeView.as_view(), name='landing_splash'),
    path('dashboard/', DashboardView.as_view(), name='home'),
    
    # Primary Navigation Pages
    path('courses/', TemplateView.as_view(template_name='courses.html'), name='courses'),
    path('calendar/', TemplateView.as_view(template_name='calendar.html'), name='calendar'),
    path('sched/', TemplateView.as_view(template_name='sched.html'), name='sched'),
    path('settings/', TemplateView.as_view(template_name='settings.html'), name='settings'),
    
    # Task & Management Routes
    path('tasks/', TaskListView.as_view(), name='tasks'),
    path('subtasks/', SubTaskListView.as_view(), name='subtasks'),
    path('notes/', NoteListView.as_view(), name='notes'),
    path('priorities/', PriorityListView.as_view(), name='priorities'),
    path('categories/', CategoryListView.as_view(), name='categories'),
    
    # Profile & Social
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/edit/', ProfileEditView.as_view(), name='profile_edit'),
    path('social-profile/', SocialProfileView.as_view(), name='social_profile'),
    
    # Billing
    path('billing/', BillingView.as_view(), name='billing'),
    
    # Task Operations
    re_path(r'^tasks/new/?$', TaskCreateView.as_view(), name='task_create'),
    path('tasks/<int:pk>/complete/', mark_task_complete, name='task_complete'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task_detail'),
    path('tasks/<int:pk>/edit/', TaskUpdateView.as_view(), name='task_update'),
    path('tasks/<int:pk>/delete/', TaskDeleteView.as_view(), name='task_delete'),
    
    # Authentication & Password Reset
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='password_reset_form.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
    
    # PWA and Allauth
    path('manifest.webmanifest', TemplateView.as_view(template_name='manifest.webmanifest', content_type='application/manifest+json'), name='manifest'),
    path('serviceworker.js', service_worker_view, name='serviceworker_compat'),
    path('service-worker.js', service_worker_view, name='service_worker'),
    path('', include('pwa.urls')), 
    path('accounts/', include('allauth.urls')),
]