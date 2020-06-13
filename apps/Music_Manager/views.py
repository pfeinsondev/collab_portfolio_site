from django.shortcuts import render, redirect
from ..Music_Manager.models import Album, Song
#--------------#
#--------------#
#--- Albums ---#
#--------------#
#--------------#

#----------------------#
#--- Get All Albums ---#
#----------------------#
def get_all_albums(request):
    restore_sessions_base_conditions(request)
    response_from_models = Album.albums.get_all_albums()
    if not response_from_models['status']:
        request.session['errors'] = response_from_models['errors']
        request.session['status'] = False
    else:
        request.session['all_albums'] = response_from_models['all_albums']
        request.session['status'] = True
    return render(request, 'all_albums.html')

#-----------------#
#--- Add Album ---#
#-----------------#
def get_new_album_data(request):
    if ('logged_in' in request.session):
        if request.session['logged_in']:
            return render(request, 'add_album.html')
        else:
            return not_authenticated(request)
    else:
        return not_authenticated(request)
    
def process_album_data(request):
    response_from_models = Album.albums.add_album(request.POST, request.FILES)
    if response_from_models['status']:
        request.session['new_album_added_bool'] = True
        return get_all_music(request)
    else:
        request.session['errors'] = response_from_models['errors'] 
        return get_new_album_data(request)
#--------------------#         
#--- Delete Album ---#
#--------------------#
def select_album_to_delete(request):
    if ('logged_in' in request.session):
        if request.session['logged_in']:
            response_from_models = Album.albums.get_all_albums()
            if response_from_models['status']:
                request.session['all_albums'] = response_from_models['all_albums']
            else:
                request.session['all_albums'] = ""
                request.session['errors'] = response_from_models['errors']
                return render(request, 'delete_album.html')
        else:
            return not_authenticated()
    else:
        return not_authenticated()
def delete_album(request):
    response_from_models = Album.albums.delete_album(request.POST)
    if response_from_models['status']:
        request.session['album_deleted_bool'] = True
        request.session['status'] = True
        request.session['errors'] = ""   
        return get_all_music(request)
    else:
        request.session['status'] = False
        request.session['errors'] = response_from_models['errors']
        return select_album_to_delete(request)


#-------------#
#-------------#
#--- Songs ---#
#-------------#
#-------------#

#---------------------#
#--- Get All Songs ---#
#---------------------#
def get_all_songs(request):
    response_from_models = Song.songs.get_all_songs()
    if response_from_models['status']:
        request.session['status'] = True
        request.session['all_songs_json'] = response_from_models['all_songs_json']
    else:
        request.session['status'] = False
        if request.session['errors']:
            errors = []
            errors.append(request.session['errors'])
            errors.append(response_from_models['errors'])
        request.session['errors'] = errors
    return render(request, 'all_songs.html')
        

#----------------#
#--- Add Song ---#
#----------------#
def get_new_song_data(request):
    if ('logged_in' in request.session):
        if request.session['logged_in']:
            response_from_models = Album.albums.get_all_albums()
            if response_from_models['status']:
                request.session['status'] = True
                request.session['albums'] = response_from_models['all_albums']
            else:
                request.session['status'] = False
                request.session['errors'] = "Cannot add a song without an album!"
            return render(request, 'add_song.html')
        else:
            return not_authenticated(request)
    else:
        return not_authenticated(request)
    
def process_song_data(request):
    response_from_models = Song.songs.add_song(request.POST)
    if response_from_models['status']:
        request.session['new_song_added_bool'] = True
        return get_all_music(request)
    else:
        request.session['errors'] = response_from_models['errors'] 
        return get_new_song_data(request)
    
#-------------------#  
#--- Delete Song ---#
#-------------------#
def select_song_to_delete(request):
    if ('logged_in' in request.session):
        if request.session['logged_in']:
            all_songs = Song.songs.get_all_songs()
            if all_songs['status']:
                request.session['songs'] = all_songs['all_songs_json']
                return render(request, 'select_song_to_delete.html')
            else:
                request.session['status'] = False
                return render(request, 'select_song_to_delete.html')
        else:
            return not_authenticated(request)
    else:
        return not_authenticated(request)
    
def delete_song(request):
    models_response = Song.songs.delete_song(request.POST)
    if models_response['status']:
        request.session['errors'] = ""
        return get_all_music(request)
    else:
        request.session['errors'] = "Unable to Delete song!"
        return select_song_to_delete(request)
    return


#-----------------#
#--- Utilities ---#
#-----------------#
def restore_sessions_base_conditions(request):
    request.session['all_albums'] = {}
    request.session['errors'] = []
    request.session['new_song_added_bool'] = False
    request.session['new_album_added_bool'] = False
    request.session['album_deleted_bool'] = False
    

#-----------------#
#--- All Music ---#
#-----------------#
def get_all_music(request):
    restore_sessions_base_conditions(request)
    response_from_models = Song.songs.get_all_music_as_json()
    if response_from_models['status']:
        request.session['status'] = True
        request.session['all_music'] = response_from_models['all_music']
    else:
        request.session['status'] = False
        request.session['errors'] = response_from_models['errors']
    return render(request, 'all_music.html')

# Not logged in method
def not_authenticated(request):
    request.session['logged_in'] = False
    request.session['status'] = False
    request.session['errors'] = []
    request.session['errors'] = "Must be logged in"
    return redirect('/login_admin')
