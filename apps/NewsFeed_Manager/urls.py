from django.urls import path
from . import views

urlpatterns = [
    path('get_all_newsfeed_entries', views.get_all_newsfeed_entries, name='get_all_newsfeed_entries'),
    path('collect_new_entry_data', views.collect_new_entry_data, name='collect_new_entry_data'),
    path('process_new_entry_data', views.process_new_entry_data, name='process_new_entry_data'),
    path('select_post_to_delete', views.select_post_to_delete, name='select_post_to_delete'),
    path('delete_post', views.delete_post, name='delete_post'),
]
