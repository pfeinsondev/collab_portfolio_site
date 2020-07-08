from django.db import models

class AboutInformationManager(models.Manager):
    
    def update_about_me(self, post_data, post_data_files):
        response_from_models = {}
        already_exists = self.filter()
        if already_exists:
            already_exists.delete()
        initial_update = self.create(about_me_text = post_data['about_me_text'], about_me_image = post_data_files['about_me_image'])
        initial_update.save()
        if initial_update:
            response_from_models['status'] = True
            response_from_models['about_me'] = initial_update
        else:
            response_from_models['status'] = False
            response_from_models['errors'] = "Failed to create initial update!"
        return response_from_models

    def get_about_me_information(self):
        response_from_models = {}
        current_information_queryset = self.filter()
        if current_information_queryset:
            current_information = {}
            current_information['about_me_image'] = current_information_queryset[0].about_me_image
            current_information['about_me_text'] = current_information_queryset[0].about_me_text
            response_from_models['status'] = True
            response_from_models['current_information'] = current_information
        else:
            response_from_models['status'] = False
            response_from_models['errors'] = "About Me Information Not Found!"
        return response_from_models
        
class AboutInformation(models.Model):
    about_me_text = models.CharField(max_length = 2000)
    about_me_image = models.ImageField(upload_to="media/")
    about_me_manager = AboutInformationManager()
        
