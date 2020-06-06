from django.db import models

#--------------#
#--- Albums ---#
#--------------#
class Album_Manager(models.Manager):
    #-----------------#
    #--- Add Album ---#
    #-----------------#
    def add_album(self, post_data, post_data_files):
        model_status = {}
        errors = []
        if not (len(post_data['album_name']) > 0):
            errors.append("Album name cannot be blank")
        if errors:
            model_status['status'] = False
        else:
            model_status['status'] = True
            # Create DB Entry
            new_album = self.create(album_name=post_data['album_name'], album_date=post_data['album_date'], album_image=post_data_files['album_image'])
            model_status['new_album'] = new_album
            new_album.save()
        return model_status
    
    #--------------------#
    #--- Delete Album ---#
    #--------------------#
    def delete_album(self, post_data):
        model_status = {}
        ### Query
        target_album_to_delete = self.filter(album_name=post_data['album_name'])
        if target_album_to_delete:
            target_album_to_delete.delete()
            model_status['status'] = True
        else:
            model_status['status'] = False
            model_status['errors'] = "Unable to Delete"
        return model_status
    
    #----------------------#
    #--- Get All Albums ---#
    #----------------------#
    def get_all_albums(self):
        model_status = {}
        all_albums = self.filter()
        print(all_albums)
        if all_albums:
            model_status['status'] = True
            all_albums_json = []
            for album in all_albums:
                album_data_json = {}
                album_data_json['album_name'] = album.album_name
                # All album names
                all_albums_json.append(album.album_name)
            model_status['all_albums'] = all_albums_json
        else:
            model_status['status'] = False
            model_status['errors'] = "No Albums Found!"
        return model_status
    
        #-------------------#
        #--- Create Json ---#
        #-------------------#
    def jsonify_album(self, album):
        album_data = {}
        album_data['album_name'] = str(album.album_name)
        album_data['album_date'] = str(album.album_date)
        album_data['album_image'] = str(album.album_image.url)
        return album_data

    
    #-------------------------#
    #--- Get Album By Name ---#
    #-------------------------#
    def get_album_by_name(self, target_album_name):
        model_status = {}
        target_album = self.get(album_name = target_album_name)
        if target_album:
            model_status['status'] = True
            model_status['target_album'] = target_album
        else:
            model_status['status'] = False
            model_status['errors'] = "Album Not Found!"
        return model_status

#-------------------#
#--- Album Model ---#
#-------------------#
class Album(models.Model):
    album_name = models.CharField(max_length=150, primary_key=True)
    album_date = models.DateField(max_length=25) 
    album_image = models.ImageField(upload_to="media/", blank = True)
    albums = Album_Manager()
#-------------#
#--- Songs ---#
#-------------#
class Song_Manager(models.Manager):
    #----------------#
    #--- Add Song ---#
    #----------------#
    def add_song(self, post_data):
        model_status = {}
        errors = []
        # Validation
        song_name_used = self.filter(song_name = post_data['song_name'])
        if song_name_used:
            errors.append("Song name already in use!")
        if not (len(post_data['song_name']) > 0):
            errors.append("Song name too short / Cannot be blank")
        if not (len(post_data['album_name']) > 0):
            errors.append("Album name cannot be blank")
        if errors:
            model_status['status'] = False
            model_status['errors'] = errors
        else:
            model_status['status'] = True
            # Create DB Entry
            parent_album_query = Album.albums.get_album_by_name(post_data['album_name']) # Ensure the parent album exists / Store reference for db entry
            if parent_album_query['status']: 
                new_song = self.create(song_name=post_data['song_name'], song_album=parent_album_query['target_album'])
                model_status['new_song'] = new_song
                new_song.save()
            else:
                model_status['status'] = False
                model_status['errors'].append("Parent album not found!")
        return model_status
    #---------------------#
    #--- Get All Songs ---#
    #---------------------#
    def get_all_songs(self):
        model_status = {}
        all_songs_queryset = self.filter()
        if all_songs_queryset:
            model_status['status'] = True
            all_songs_json = []
            for song in all_songs_queryset:
                song_details = {}
                song_details['song_name'] = song.song_name
                song_details['album'] = song.song_album.album_name
                all_songs_json.append(song_details)
            model_status['all_songs_json'] = all_songs_json
        else:
            model_status['status'] = False
            model_status['errors'] = "No songs found!"
        return model_status
    
    #-------------------#
    #--- Delete Song ---#
    #-------------------#
    def delete_song(self, post_data):
        model_status = {}
        ### Query
        target_song_to_delete = self.filter(song_name=post_data['song_name_to_delete'])
        if target_song_to_delete:
            model_status['status'] = True
            target_song_to_delete.delete()
        else:
            model_status['status'] = False
        return model_status
    
    #-------------------------#
    #--- Get Song By Album ---#
    #-------------------------#
    def get_all_song_on_album(self, target_album):
        model_status = {}
        ### Query
        songs_on_target_album = self.filter(song_album=target_album)
        if songs_on_target_album: # Success Path
            model_status['status'] = True # Set model_status['status'] True
            list_of_songs_on_album = [] # Will store all songs on album
            song_details = {} # Dictionary<String, String>
            for song in songs_on_target_album:
                song_details['song_name'] = song.song_name
                list_of_songs_on_album.append(song_details)
                song_details = {}
            model_status['all_songs_on_album'] = list_of_songs_on_album # List<Dictionary<String, String>>
        else:
            model_status['status'] = False
            model_status['errors'] = "No songs found! Have you added any?"
        return model_status
    
    #------------------------#
    #--- Get Song By Name ---#
    #------------------------#
    def get_song_by_name(self, target_song_name):
        model_status = {}
        target_song = self.filter(song_name = target_song_name)
        if target_song:
            model_status['status'] = True
            model_status['target_song'] = target_song
        else:
            model_status['status'] = False
            model_status['errors'] = "Song not found"
        return model_status
    
    #---------------------#
    #--- Get All Music ---#
    #---------------------#
    def get_all_music_as_json(self):
        all_songs = self.filter()
        model_status = {} # Returned Dictionary
        all_albums = Album.albums.filter() # Get 'model_status' from Album.albums.get_all_albums()
        if all_albums: # Success Path
            all_music = {} # all_music dictionary will be assigned to model_status['all_music']
            model_status['status'] = True
            for album in all_albums: # iterate through all albums
                album_details = {}
                album_details['album_name'] = album.album_name
                album_details['album_image'] = album.album_image.url
                album_details['album_date'] = str(album.album_date)
                album_details['album_songs'] = []
                songs_on_album = self.filter(song_album = album) # query for all songs that belong to the album
                songs_on_album_json = [] # List of Dictionary<String, String>
                
                if songs_on_album: # If there are songs on the album
                    for song in songs_on_album: # Compile Json for each song
                        song_details = {} # Dictionary<String, String> of song details
                        song_details['song_name'] = song.song_name
                        album_details['album_songs'].append(song_details)
                all_music[album.album_name] = album_details # Assign each album (key) songs_on_album_json (value)
            model_status['all_music'] = all_music 
        else:
            model_status['status'] = False # Fail Path
            model_status['errors'] = "No music found!"
        return model_status
                
#------------------#
#--- Song Model ---#
#------------------#
class Song(models.Model):
    song_name = models.CharField(max_length=150, primary_key=True)
    song_album = models.ForeignKey(to=Album, on_delete=models.CASCADE)
    songs = Song_Manager()
