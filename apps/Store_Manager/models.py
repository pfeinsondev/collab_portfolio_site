from django.core.files.storage import FileSystemStorage
from django.db import models

class Store_Manager(models.Manager):
    #---------------------#
    #--- Get All items ---#
    #---------------------#
    def get_all_items(self):
        model_status = {}
        all_items = self.filter()
        if all_items:
            # Create Json of all store all_items
            all_items_list = []      # Every Item as an "item"
            all_items_json = []      # Every Item
            item_details_json = {}   # Individual item Details
            for item in all_items:
                all_items_list.append(item)
                item_details_json = {}
                item_details_json['item_name'] = item.item_name
                item_details_json['item_image'] = item.item_image.url
                item_details_json['item_price'] = str(item.item_price)
                item_details_json['item_description'] = item.item_description
                all_items_json.append(item_details_json)
            model_status['status'] = True
            model_status['all_items'] = all_items_json
            model_status['all_items_list'] = all_items_list
        else:
            model_status['status'] = False
            model_status['errors'] = "No items Found!"
        return model_status
    
    #----------------#
    #--- Add Item ---#
    #----------------#
    def add_item(self, post_data, post_data_files):
        model_status = {}
        # Validation
        errors = []
        if (len(post_data['item_name']) < 1):
            errors.append("Item Name must be at least 1 character")
        if (float(post_data['item_price']) < 0):
            errors.append("Item price cannot be less than 0")
        if (len(post_data['item_description']) < 1):
            errors.append("Item Description cannot be blank!")
        if errors:
            model_status['status'] = False
            model_status['errors'] = errors
        else:
            model_status['status'] = True
            new_item = self.create(item_name = post_data['item_name'], item_image=post_data_files['item_image'], item_price = post_data['item_price'], item_description = post_data['item_description'])
            new_item.save()
            model_status['new_item'] = new_item
        return model_status
    #---------------------------------#
    #--- Get All Item Names (keys) ---#
    #---------------------------------#
    def get_all_item_names(self):
        model_status = {}
        all_items = self.filter()
        if all_items:
            all_item_names = [] 
            for item in all_items:
                all_item_names.append(item.item_name)
            model_status['status'] = True
            model_status['all_item_names'] = all_item_names
        else:
            model_status['status'] = False
            model_status['errors'] = "No items found!"
        return model_status
        
    #-------------------#
    #--- Delete Item ---#
    #-------------------#
    def delete_item(self, target_name):
        model_status = {}
        target_name_query = self.filter(item_name=target_name)
        if target_name_query:
            model_status['status'] = True
            target_name_query.delete()
        else:
            model_status['status'] = False
            model_status['errors'] = "Entry not found"
        return model_status
        
class Store(models.Model):
    item_name = models.CharField(max_length=250, primary_key = True)
    item_image = models.ImageField(upload_to="media/")
    item_price = models.FloatField()
    item_description = models.CharField(max_length=500)
    stores = Store_Manager()
