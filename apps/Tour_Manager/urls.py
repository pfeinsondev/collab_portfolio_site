from django.urls import path
from . import views

urlpatterns = [
    path('all_tours', views.all_tours, name='all_tours'),
    path('get_new_tour_data', views.get_new_tour_data, name='get_new_tour_data'),
    path('create_new_tour', views.create_new_tour, name='create_new_tour'),
    path('get_new_show_data', views.get_new_show_data, name='get_new_show_data'),
    path('create_new_show', views.create_new_show, name='create_new_show'),
    path('remove_show', views.remove_show, name='remove_show'),
    path('remove_tour', views.remove_tour, name='remove_tour'),
    path('select_show_to_delete', views.select_show_to_delete, name='select_show_to_delete'),
    path('select_tour_to_delete', views.select_tour_to_delete, name='select_tour_to_delete'),
    path('get_all_shows', views.get_all_shows, name='get_all_shows'),
    path('delete_show', views.remove_show, name='delete_show'),
]
