from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Dashboards
    path('superadmin/', views.superadmin_dashboard, name='superadmin_dashboard'),
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    path('user/', views.user_dashboard, name='user_dashboard'),

    # Admin Task Management (Admin can manage tasks for users)
    path('admin/create-task/', views.create_task, name='create_task'),
    path('admin/edit-task/<int:pk>/', views.admin_edit_task, name='admin_edit_task'),
    path('admin/delete-task/<int:pk>/', views.admin_delete_task, name='admin_delete_task'),  # reuse delete_task view
    path('admin/task-report/<int:pk>/', views.view_report, name='admin_view_report'),  # reuse view_report view

    # User Task Management
    path('user/complete-task/<int:pk>/', views.complete_task, name='complete_task'),
    path('task/<int:pk>/report/', views.view_report, name='view_report'),

    # SuperAdmin: User/Admin Management
    path('superadmin/manage-users/', views.manage_users, name='manage_users'),
    path('superadmin/add-user/', views.add_user, name='add_user'),
    path('superadmin/edit-user/<int:pk>/', views.edit_user, name='edit_user'),
    path('superadmin/delete-user/<int:pk>/', views.delete_user, name='delete_user'),
    path('superadmin/change-admin-role/<int:pk>/', views.change_admin_role, name='change_admin_role'),

    # SuperAdmin Task Management
    path('superadmin/tasks/', views.superadmin_tasks, name='superadmin_tasks'),
    path('superadmin/tasks/add/', views.add_task, name='add_task'),
    path('superadmin/tasks/edit/<int:pk>/', views.edit_task, name='edit_task'),
    path('superadmin/tasks/delete/<int:pk>/', views.delete_task, name='delete_task'),
    path('superadmin/tasks/report/<int:pk>/', views.view_task_report, name='view_task_report'),
]
