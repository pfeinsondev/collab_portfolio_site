from django.contrib.auth.hashers import make_password, check_password
from django.db import models
import re


class Admin_Manager(models.Manager):
    # post_data must contain (first_name, last_name, recovery_email, password, password_confirmation, username)
    # admin registration route
    def validate_and_register_admin(self, post_data):
        errors = []
        # Validate username
        if not (len(post_data['username']) > 6):
            errors.append("Username must be at least 7 characters long")
        # First name validation
        if not (len(post_data['first_name']) >= 2 and re.match("^[a-zA-Z]", post_data['first_name'])):
            errors.append("First name too short")
        # Last name valiation
        if not (len(post_data['last_name']) >= 2 and re.match("^[a-zA-Z]", post_data['last_name'])):
            errors.append("Last name too short")
        # Email Address Validation
        if not re.match("^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$", post_data['recovery_email']):
            errors.append("Invalid Email-Address must use format: example@example.example")
        # Validate Password
        if not (len(post_data["password"]) >= 5):
            errors.append("Password too short")
        if not (post_data['password'] == post_data['password_confirmation']):
            errors.append("Passwords do not match")
        # Prepare return data   
        model_status = {}
        # If there are errors, return them
        if errors:
            model_status['status'] = False
            model_status['errors'] = errors
        # If everything checks out, go ahead and create the admin acount
        else: 
            # Hash password
            hashed_password = make_password(post_data['password'])
            # Create Admin
            admin = self.create(username = post_data['username'], first_name = post_data['first_name'], last_name = post_data['last_name'], password = hashed_password,
                               recovery_email = post_data['recovery_email'])
            admin.save()
            model_status['status'] = True
            model_status['admin'] = admin
            
        return model_status

    def login(self, post_data):
        # Check if user is in db
        admin = self.filter(username=post_data['username'])
        models_response = {}
        # if admin exists
        if admin:
            if (check_password(post_data['password'], admin[0].password)):
                # send success to views
                models_response['status'] = True
                models_response['admin'] = admin
            else:
                # send message to views
                models_response['status'] = False
                models_response['errors'] = "Invalid Password!"
        else: 
            models_response['status'] = False
            models_response['errors'] = "Username not found!"
            
        return models_response
                
class Admin(models.Model):
    username = models.CharField(max_length=45)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    password = models.CharField(max_length=45)
    recovery_email = models.CharField(max_length=100)
    password_last_updated = models.DateTimeField(auto_now=True)
    admins = Admin_Manager()
