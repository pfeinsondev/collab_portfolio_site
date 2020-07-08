from django.core.files.storage import FileSystemStorage
from django.db import models
from django import forms

class NewsFeed_Manager(models.Manager):
    #--------------------#
    #    Get all Query   #
    #--------------------#
    def get_all_entries(self):
        model_status = {}
        all_entries = self.filter()
        if all_entries:
            # Build returnable data
            entries_list_json = []
            for entry in all_entries:
                individual_entry_json = {}
                # Date/Time Formatting
                date_fragments = str(entry.post_date).split("-")
                human_readable_date = date_fragments[1] + "-" + date_fragments[2] + "-" + date_fragments[0]
                individual_entry_json['post_date'] = human_readable_date
                time_fragments = str(entry.post_time).split(":")
                if int(time_fragments[0]) > 12:
                    time_fragments[0] = str(int(time_fragments[0])-12)
                    time_period = "PM"
                else:
                    time_period = "AM"
                human_readable_time = time_fragments[0] + ":" + time_fragments[1] + " " + time_period
                individual_entry_json['post_time'] = human_readable_time
                individual_entry_json['post_media'] = entry.post_media.url
                individual_entry_json['post_id'] = entry.id
                entries_list_json.append(individual_entry_json)
            # Update Model Status, json:
            #       entries_list_json:
            #           [ {post_content:<String>, post_date:<String>, post_media:<url>} ]
            model_status['status'] = True
            model_status['entries_list_json'] = entries_list_json
        else:
            model_status['status'] = False
            model_status['errors'] = "No posts found!"
        return model_status
    #----------------------#
    #   Create New Entry   #
    #----------------------#
    def create_new_entry(self, post_data_files):
        model_status = {}
        errors = []
        if errors:
            model_status['status'] = False
            model_status['errors'] = errors
        else:
            entry = self.create(post_media=post_data_files['post_media'])
            entry.save()
            model_status['status'] = True
            model_status['new_entry'] = entry
        return model_status

    #------------------#
    #   Delete Entry   #
    #------------------#
    def delete_entry(self, post_data):
        model_status = {}
        target_entry = self.filter(id=post_data['target_entry_id'])
        if target_entry:
            target_entry.delete()
            model_status['status'] = True
        else:
            model_status['errors'] = "Target Entry Not Found"
            model_status['status'] = False
        return model_status
    
#--------------------#
#   Newsfeed Model   #
#--------------------#
class NewsFeed(models.Model):
    post_date = models.DateField(auto_now=True)
    post_time = models.TimeField(auto_now=True)
    post_media = models.FileField(upload_to="media/")
    newsfeed_manager = NewsFeed_Manager()
