from django.urls import path
from . import views

urlpatterns = [
    # Get All Songs
    path('get_all_songs', views.get_all_songs, name='get_all_songs'),
    # Get All Music
    path('all_music', views.get_all_music, name="all_music"),
    # Add Album
    path('get_new_album_data', views.get_new_album_data, name="get_new_album_data"),
    path('process_album_data', views.process_album_data, name="process_album_data"),
    # Add Song
    path('get_new_song_data', views.get_new_song_data, name="get_new_song_data"),
    path('process_song_data', views.process_song_data, name="process_song_data"),
    # Delete Album
    path('select_album_to_delete', views.select_album_to_delete, name="select_album_to_delete"),
    path('delete_album', views.delete_album, name='delete_album'),
    # Delete Song
    path('select_song_to_delete', views.select_song_to_delete, name="select_song_to_delete"),
    path('delete_song', views.delete_song, name="delete_song"),    
]
