from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [

   
    path('', views.login, name='login'),
    path('login', views.login, name='login'),
    path('do_login', views.do_login, name='do_login'),
    path('logout_user', views.logout_user, name='logout_user'),
    path('admin_home', views.admin_home, name='admin_home'),
    path('emp_home', views.emp_home, name='emp_home'),
    path('admin_profile', views.admin_profile, name="admin_profile"),
    path('admin_profile_update', views.admin_profile_update, name="admin_profile_update"),
    path('emp_profile', views.emp_profile, name="emp_profile"),
    path('emp_profile_update', views.emp_profile_update, name="emp_profile_update"),
    path('manage_emp', views.manage_emp, name="manage_emp"),
    path('add_emp', views.add_emp, name='add_emp'),
    path('add_emp_save', views.add_emp_save, name='add_emp_save'),
    path('activate_deactivate_emp', views.activate_deactivate_emp, name='activate_deactivate_emp'),
    path('edit_emp', views.add_emp, name="edit_learner"),
    #path('edit_emp_save', views.edit_emp_save, name="edit_learner_save"),
    path('delete_emp/<id>', views.delete_emp, name="delete_emp"),
    path('check_email_exist', views.check_email_exist, name="check_email_exist"),
    path('check_username_exist',views.check_username_exist, name="check_username_exist"),
    path('edit_emp/<id>', views.edit_emp, name="edit_emp"),
    path('edit_emp_save', views.edit_emp_save, name="edit_emp_save"),
    path('deactivate_emp/<id>', views.deactivate_emp, name="deactivate_emp"),
    path('activate_emp/<id>', views.activate_emp, name="activate_emp"),
]