from django.urls import path
from . import views

urlpatterns = [
    path('all_art', views.get_all_art, name='all_art'),
    path('get_new_art_details', views.get_new_art_details, name='get_new_art_details'),
    path('process_new_art', views.process_new_art, name='process_new_art'),
    path('select_art_to_delete', views.select_art_to_delete, name='select_art_to_delete'),
    path('delete_art', views.delete_art, name='delete_art'),
    ]
