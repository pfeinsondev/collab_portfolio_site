from django.shortcuts import render
from ..Admin_Manager.models import Admin
from ..Front_End.models import AboutInformation

#--------------------------#
#--- Admin Landing Page ---#
#--------------------------#
def admin_index(request):
    return render(request, 'admin_index.html')

#-----------------------#
#--- Admin Form Page ---#
#-----------------------#
def admin_login(request):
    return render(request, 'login.html')

#--------------------------------#
#--- Process Admin Login Form ---#
#--------------------------------#
def authenticate_admin(request):
    response_from_models = Admin.admins.login(request.POST)
    if response_from_models['status']:
        return render(request, 'admin_index.html')
    else:
        request.session['errors'] = response_from_models['errors']
        return admin_login(request)


#-------------------------------#
#--- Admin Registration Form ---#
#-------------------------------#
    
def collect_new_admin_data(request):
    return render(request, 'register.html')

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
        return collect_new_admin_data(request)

#----------------------------------------#
#--- Admin Registration Success Route ---#
#----------------------------------------#
def registration_success(request):      
    return render(request, 'registration_success.html')

def reset_password_request(request):
    return
#----------------------------------------#
#--- Get Current About Me Information ---#
#----------------------------------------#
def get_current_about_me_data(request):
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

#---------------------------------#
#--- Update About Me Form Page ---#
#---------------------------------#
def collect_new_about_me_data(request):
    response_from_models = AboutInformation.about_me_manager.get_about_me_information()
    if response_from_models['status']:
        current_information = response_from_models['current_information']
        request.session['about_me_text'] = current_information['about_me_text']
        request.session['status'] = True
    else:
        request.session['errors'] = response_from_models['errors']
        request.session['status'] = False
    return render(request, 'admin_update_about_me.html')

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
