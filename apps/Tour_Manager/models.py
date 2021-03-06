from django.db import models

#-------------#
#--- Tours ---#
#-------------#
class Tour_Manager(models.Manager):
    #----------------#
    #--- Add Tour ---#
    #----------------#
    def add_tour(self, post_data, post_data_files):
        model_status = {}
        if not (len(post_data['tour_name']) > 0):
            model_status['status'] = False
            model_status['errors'] = "Tour name must not be blank"
        else:
            new_tour_check = self.filter(tour_name=post_data['tour_name'])
            if new_tour_check:
                model_status['status'] = False
                model_status['errors'] = "Tour already exists"
            else:
                new_tour = self.create(tour_name=post_data['tour_name'], tour_image=post_data_files['tour_image'])
                model_status['status'] = True
                model_status['tour_name'] = new_tour
                new_tour.save()
        return model_status
    #------------------------#
    #--- Get Tour by Name ---#
    #------------------------#
    def get_tour(self, post_data):
        target_tour = self.get(tour_name=post_data['tour_name'])
        tour_status = {}
        if target_tour:
            tour_status['status'] = True
            tour_status['target_tour'] = target_tour
        else:
            tour_status['status'] = False
        return tour_status
    #---------------------#
    #--- Get All tours ---#
    #---------------------#
    def get_all_tours(self):
        all_tours = self.filter()
        # Json Packaging information
        tour_json = {} # 'tour1' : tour_catalog; Final object structure: Dictionary<String, List<Dictionary<String, String>>>
        model_status = {}
        #for tour in all_tours:
        #    tour_names.append(tour['tour_name'])
        if all_tours:
            model_status['status'] = True
            all_tours_list = []
            for tour in all_tours:
                tour_json = {}
                tour_json['shows'] = Show.shows.get_shows_by_tour(tour.id)
                tour_json['tour_name'] = tour.tour_name
                tour_json['tour_image'] = tour.tour_image.url
                all_tours_list.append(tour_json) 
                
            model_status['tours'] = all_tours_list
        else:
            model_status['status'] = False
            model_status['errors'] = "No Tours Found!"
        return model_status
    #-------------------#
    #--- Remove Tour ---#
    #-------------------#
    def remove_tour(self, post_data):
        model_status = {}
        target_to_remove = self.filter(tour_name=post_data['tour_name'])
        if target_to_remove:
            model_status['status'] = True
            target_to_remove.delete()
        else:
            model_status['status'] = False
            model_status['errors'] = "Tour not found, cannot delete"
        return model_status
#------------------#
#--- Tour model ---#
#------------------#
class Tour(models.Model):
    tour_name = models.CharField(max_length=200)
    tour_image = models.ImageField(upload_to="media/", blank = True)
    tours = Tour_Manager()
    
#-------------#
#--- Shows ---#
#-------------#
class Show_Manager(models.Manager):
    #----------------#
    #--- Add Show ---#
    #----------------#
    def add_show(self, post_data):
        model_status = {}
        errors = []
        if not (len(post_data['show_city'])) > 0:
            errors.append("City cannot be empty")
        if not (len(post_data['show_state']) == 2):
            errors.append("Invalid city code, please use 2 character format (VT = Vermont)")
        if errors:
            model_status['status'] = False
            model_status['errors'] = errors
        else:
            response_from_tour_manager = Tour.tours.get_tour(post_data)
            parent_tour = response_from_tour_manager['target_tour']
            show = self.create(show_city=post_data['show_city'], show_state=post_data['show_state'], show_time=post_data['show_time'], show_date=post_data['show_date'], tour=parent_tour)
            show.save()
            model_status['status'] = True
            model_status['show'] = self.jsonify_show(show)
        return model_status     

    #-------------------#
    #--- Delete Show ---#
    #-------------------#
    def delete_show(self, target_show):
        target_to_delete = self.filter(id=target_show)
        model_status = {}
        if target_to_delete:
            target_to_delete.delete()
            model_status['status'] = True
        else:
            model_status['status'] = False
            model_status['errors'] = "Unable to delete show"
        return model_status
    #---------------------#
    #--- Get All Shows ---#
    #---------------------#
    def get_all_shows(self):
        all_shows = self.filter()
        model_status = {}
        if all_shows:
            show_catalog = []
            for show in all_shows:
                show_catalog.append(Show.shows.jsonify_show(show))
            model_status['status'] = True
            model_status['shows'] = show_catalog
        else:
            model_status['status'] = False
            model_status['errors'] = "No Shows Found!"
            model_status['shows'] = {}
        return model_status
    #-------------------------#
    #--- Get Shows By Tour ---#
    #-------------------------#
    def get_shows_by_tour(self, target_tour_id):
        tour_object_by_id = Tour.tours.filter(id=target_tour_id)
        all_shows = self.filter(tour=tour_object_by_id[0])
        shows_json_list = []
        for show in all_shows:
            shows_json_list.append( Show.shows.jsonify_show(show) )
        return shows_json_list
        #------------------------------------------------------------#
        #--- Jsonify Show ---> Packages Show data to a dictionary ---#
        #------------------------------------------------------------#
    def jsonify_show(self, show):
        json_show_data = {}
        json_show_data['show_city'] = show.show_city
        json_show_data['show_state'] = show.show_state
        #-
        # Time Formatting
        #- 
        time_fragments = str(show.show_time).split(":")
        if int(time_fragments[0]) > 12:
            time_fragments[0] = str(int(time_fragments[0])-12)
            time_period = "PM"
        else:
            time_period = "AM"
        human_readable_time = time_fragments[0] + ":" + time_fragments[1] + " " + time_period
        json_show_data['show_time'] = human_readable_time
        #-
        # Date Formatting 
        #- 
        date_fragments = str(show.show_date).split("-")
        human_readable_date = date_fragments[1] + "-" + date_fragments[2] + "-" + date_fragments[0]
        json_show_data['show_date'] = human_readable_date
        json_show_data['tour'] = show.tour.id
        return json_show_data
#------------------#
#--- Show Model ---#
#------------------#
class Show(models.Model):
    show_city = models.CharField(max_length=100)
    show_state = models.CharField(max_length=3)
    show_time = models.TimeField(max_length=25)
    show_date = models.DateField(max_length=25)
    tour = models.ForeignKey(to=Tour, on_delete=models.CASCADE)
    shows = Show_Manager()
