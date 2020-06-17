from django.urls import path
from . import views

urlpatterns = [
    path('login_admin', views.admin_login, name='login_admin'),
    path('authenticate_admin', views.authenticate_admin, name='authenticate_admin'),
    path('collect_new_admin_data', views.collect_new_admin_data, name='collect_new_admin_data'),
    path('register_new_admin', views.register_new_admin, name='register_new_admin'),
    path('reset_password_request', views.reset_password_request, name='reset_password_request'),
    path('get_current_about_me_data', views.get_current_about_me_data, name='get_current_about_me_data'),
    path('collect_new_about_me_data', views.collect_new_about_me_data, name='collect_new_about_me_data'),
    path('process_new_about_me_data', views.process_new_about_me_data, name='process_new_about_me_data'),
    path('override_authentication', views.override_authentication, name='override_authentication'), 
    path('process_override_authentication', views.process_override_request, name='process_override_authentication'),
    path('admin_index', views.admin_index, name='admin_index'),
]
