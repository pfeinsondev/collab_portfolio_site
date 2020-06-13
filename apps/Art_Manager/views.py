from __future__ import unicode_literals
from django.shortcuts import render, redirect
from ..Art_Manager.models import Art

def get_all_art(request):    
    response_from_model = Art.arts.get_all_art()
    if response_from_model['status']:
        request.session['status'] = True
        request.session['all_art'] = response_from_model['all_art']
    else:
        request.session['status'] = False
        request.session['errors'] = response_from_model['errors'] 
    return render(request, 'all_art.html')
    
def get_new_art_details(request):
    if ('logged_in' in request.session):
        if request.session['logged_in']:
            request.session['status'] = True
            return render(request, 'add_art.html')
        else:
            request.session['status'] = False
            request.session['errors'] = []
            request.session['errors'].append("must be logged in ")
            return redirect('/login_admin')
    else:
        return not_authenticated()
    
def process_new_art(request):
    response_from_model = Art.arts.add_art(request.POST, request.FILES)
    if response_from_model['status']:
        request.session['status'] = True
        return get_all_art(request)
    else:
        request.session['status'] = False
        request.session['errors'] = response_from_model['errors']
        return render(request, 'add_art.html') 

def select_art_to_delete(request):
    if ('logged_in' in request.session):
        if request.session['logged_in']:
            response_from_model = Art.arts.get_all_art()
            if response_from_model['status']:
                request.session['all_art'] = response_from_model['all_art']
                request.session['status'] = True
            else:
                request.session['status'] = False
                request.session['errors'] = response_from_model['errors']
            return render(request, 'select_art_to_delete.html')
        else:
            return not_authenticated()
    else:
        return not_authenticated()
    
def delete_art(request):
    response_from_model = Art.arts.delete_art(request.POST)
    if response_from_model['status']:
        request.session['status'] = True
        return select_art_to_delete(request)
    else:
        request.session['status'] = False
        request.session['errors'] = response_from_model['errors']
    return render(request, 'select_art_to_delete.html')

# Not logged in method
def not_authenticated(request):
    request.session['status'] = False
    request.session['errors'] = []
    request.session['errors'] = "Must be logged in"
    return redirect('/admin-login')
