from django.shortcuts import render, redirect
from .models import Admin
from ..Front_End.models import AboutInformation

#-----------------------------------------------------------------------------#
#----------                         Admin Pages                     ----------#
#-----------------------------------------------------------------------------#

#--------------------------#
#--- Admin Landing Page ---#
#--------------------------#
def admin_index(request):
    if ('logged_in' in request.session):
        if request.session['logged_in']:
            return render(request, 'admin_index.html')
        else:
            return not_authenticated(request)
    else:
        return not_authenticated()
#-----------------------#
#--- Admin Form Page ---#
#-----------------------#
def admin_login(request):
    if not ('logged_in' in request.session):
        request.session['logged_in'] = False
    return render(request, 'login.html')

#--------------------------------#
#--- Process Admin Login Form ---#
#--------------------------------#
def authenticate_admin(request):
    response_from_models = Admin.admins.login(request.POST)
    if response_from_models['status']:
        request.session['status'] = True
        request.session['logged_in'] = True
        return render(request, 'admin_index.html')
    else:
        request.session['status'] = False
        request.session['logged_in'] = False
        request.session['errors'] = response_from_models['errors']
        return admin_login(request)


#-------------------------------#
#--- Admin Registration Form ---#
#-------------------------------#
    
def collect_new_admin_data(request):
    # Override Code "override_admin_registration_lock"
    if ('logged_in' in request.session):
        if (request.session['logged_in']):
            return render(request, 'register.html')
        else:
            return not_authenticated()
    else:
        return not_authenticated(request)
    
#---------------------------------------#
#--- Process Admin Registration Form ---#
#---------------------------------------#
def register_new_admin(request):
    # Attempt to validate and register
    response_from_models =  Admin.admins.validate_and_register_admin(request.POST)
    # Success State
    if response_from_models['status']:
        request.session['registration_success'] = True
        return registration_success(request)
    else:
        request.session['status'] = False
        request.session['errors'] = response_from_models['errors']        
        return render(request, 'login.html')

#----------------------------------------#
#--- Admin Registration Success Route ---#
#----------------------------------------#
def registration_success(request):      
    return render(request, 'registration_success.html')

def reset_password_request(request):
    return

#----------------------------------------------------#
#--- First time registration / Forced access code ---#
#----------------------------------------------------#

def override_authentication(request):
    request.session['errors'] = ""
    return render(request, 'override_authentication.html')

def process_override_request(request):
    if (request.POST['force_code'] == "override_admin_registration_lock"):
        request.session['status'] = True
        request.session['logged_in'] = True
        return collect_new_admin_data(request)
    else:
        request.session['status'] = False
        request.session['errors'] = "Invalid override authentication code, try again"
        return render(request, 'override_authentication.html')
    
    
#---------------#
#--- Log out ---#
#---------------#

def log_out(request):
    request.session['logged_in'] = False
    request.session['status'] = False
    request.session['errors'] = "Successfully logged out!"
    return render(request, 'login.html')
    
#------------------------------------------------------------------------------#
#----------                         About Me Pages                  -----------#
#------------------------------------------------------------------------------#

#----------------------------------------#
#--- Get Current About Me Information ---#
#----------------------------------------#
def get_current_about_me_data(request):
    if ('logged_in' in request.session):
        if request.session['logged_in']:
            response_from_models = AboutInformation.about_me_manager.get_about_me_information()
            if response_from_models['status']:
                current_information = response_from_models['current_information']
                request.session['about_me_text'] = current_information['about_me_text']
                request.session['about_me_image'] = current_information['about_me_image'].url
                request.session['status'] = True
            else:
                request.session['errors'] = response_from_models['errors']
                request.session['status'] = False
            return render(request, 'admin_about_me.html')
    else:
        request.session['status'] = False
        request.session['errors'] = []
        request.session['errors'].append("must be logged in ")
        return admin_login(request)
        
#---------------------------------#
#--- Update About Me Form Page ---#
#---------------------------------#
def collect_new_about_me_data(request):
    if ('logged_in' in request.session):
        if request.session['logged_in']:
            response_from_models = AboutInformation.about_me_manager.get_about_me_information()
            if response_from_models['status']:
                current_information = response_from_models['current_information']
                request.session['about_me_text'] = current_information['about_me_text']
                request.session['status'] = True
            else:
                request.session['errors'] = []
                request.session['errors'] = response_from_models['errors']
                request.session['status'] = False
                return render(request, 'admin_update_about_me.html')
        else:
            return not_authenticated(request)
    else:
        return not_authenticated(request)
    
#------------------------------------#
#--- Process Update About Me Form ---#
#------------------------------------#
def process_new_about_me_data(request):
    response_from_models = AboutInformation.about_me_manager.update_about_me(request.POST, request.FILES)
    if response_from_models['status']:
        request.session['status'] = True
        request.session['about_me_image'] = response_from_models['about_me'].about_me_image.url
        request.session['about_me_text'] = response_from_models['about_me'].about_me_text
        request.session['errors'] = "About Me successfully updated!"
        return render (request, 'admin_about_me.html')
    else:
        request.session['status'] = False
        request.session['errors'] = response_from_models['errors']
        return render(request, 'admin_update_about_me.html')

# Not logged in method
def not_authenticated(request):
    request.session['status'] = False
    request.session['errors'] = []
    request.session['errors'] = "Must be logged in"
    return redirect('/login_admin')
