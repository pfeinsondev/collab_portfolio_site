# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
class Art_Manager(models.Manager):
    def add_art(self, post_data, post_data_files):
        models_response = {}
        errors = []
        if not post_data_files['art_image']:
            errors.append("No Image found!")
        if not post_data['art_name']:
            post_data['art_name'] = "Un-named"
        if not errors:
            new_art = self.create(art_image=post_data_files['art_image'], art_name=post_data['art_name'], art_date = post_data['art_date'])
            new_art.save()
            if new_art:
                models_response['status'] = True
                models_response['new_art'] = new_art
            else:
                models_response['status'] = False
                models_response['errors'] = "Failed to Create!"
        else:
            models_response['status'] = False
            models_response['errors'] = errors
        return models_response
    
    def delete_art(self, post_data):
        model_response = {}
        target_art = self.filter(id=post_data['art_id_to_delete'])
        if target_art:
            target_art.delete()
            if target_art:
                model_response['status'] = False
                model_response['errors'] = "Delete Failed!"
            else:
                model_response['status'] = True
        else:
            model_response['status'] = False
            model_response['errors'] = "No art found!"
        return model_response
    
    def get_all_art(self):
        model_response = {}
        all_art_queryset = self.filter()
        if all_art_queryset:
            model_response['status'] = True
            all_art = []
            for art in all_art_queryset:
                art_details = {}
                art_details['art_name'] = art.art_name
                art_details['art_image'] = art.art_image.url
                art_details['id'] = art.id
                # Date Formatting
                date_fragments = str(art.art_date).split("-")
                human_readable_date = date_fragments[1] + "-" + date_fragments[2] + "-" + date_fragments[0]
                art_details['art_date'] = human_readable_date
                all_art.append(art_details)
            model_response['all_art'] = all_art
        else:
            model_response['status'] = False
            model_response['errors'] = "No Art Found!"
        return model_response
    
    def get_art_by_id(self, target_id):
        model_response = {}
        target_art_object = self.filter(id=target_id)[0]
        if target_art_object:
            model_response['status'] = True
            model_response['art_image'] = target_art_object.art_image.url
            model_response['art_name'] = target_art_object.art_name
            # Date/Time Formatting
            date_fragments = str(entry.post_date).split("-")
            human_readable_date = date_fragments[1] + "-" + date_fragments[2] + "-" + date_fragments[0]
            model_response['art_date'] = human_readable_date
        else:
            model_response['status'] = False
            model_response['errors'] = "Art Object Not Found!"
        return model_response
    

class Art (models.Model):
    art_image = models.FileField(upload_to="media/")
    art_name = models.CharField(max_length=100)
    art_date = models.DateField(max_length=25) 
    arts = Art_Manager()
