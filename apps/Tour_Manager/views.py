from django.shortcuts import render, redirect
from ..Tour_Manager.models import Tour, Show
#------------------#
#----- Tours ------#
#------------------#

# View for showing all tours + shows
def all_tours(request):
    #request.session['tours'] = Tour.tours.get_all_tours
    response_from_models = Tour.tours.get_all_tours()
    if response_from_models['status']:
        request.session['tours'] = response_from_models['tours']
        request.session['status'] = True
    else:
        request.session['errors'] = response_from_models['errors']
        request.session['status'] = False
    return render(request, 'all_tours.html')

# Form for getting new tour data
def get_new_tour_data(request):
    request.session['status'] = True
    return render(request, 'add_tour.html')

# Action for Creating a new tour
def create_new_tour(request):
    response_from_models = Tour.tours.add_tour(request.POST, request.FILES)
    if not response_from_models['status']:
        request.session['status'] = False
        request.session['errors'] = response_from_models['errors']
        return render(request, 'add_tour.html')
    else:
        request.session['status'] = True
        request.session['tour_added_bool'] = True
        return all_tours(request)

# Action for marking tour to remove
def select_tour_to_delete(request):
    response_from_models = Tour.tours.get_all_tours()
    if response_from_models['status']:
        request.session['errors'] = ""
        request.session['status'] = True
        request.session['tours'] = response_from_models['tours']
    else:
        request.session['errors'] = response_from_models['errors']
        request.session['status'] = False
    return render(request, 'remove_tour.html')

# Action for removing a tour from catalog
def remove_tour(request):
    response_from_models = Tour.tours.remove_tour(request.POST)
    if not response_from_models['status']:
        request.session['errors'] = response_from_models['errors']
        return select_tour_to_delete(request)
    else:
        delete_session(request)
        return all_tours(request)


#------------------#
#----- Shows ------#
#------------------#

# Form for adding a new show
def get_new_show_data(request):
    response_from_models = Tour.tours.get_all_tours()
    if response_from_models['status']:
        request.session['status'] = True
        request.session['tours'] = response_from_models['tours']
    else:
        request.session['status'] = False
        request.session['errors'] = response_from_models['errors']
    return render(request, 'add_show.html')

# Action for creating a new show
def create_new_show(request):
    response_from_models =  Show.shows.add_show(request.POST)
    if not response_from_models['status']:
        request.session['status'] = False
        request.session['errors'] = response_from_models['errors']
        return render(request, 'add_show.html')
    else: 
        request.session['status'] = True
        return get_all_shows(request)

# Display all shows
def get_all_shows(request):
    response_from_models = Show.shows.get_all_shows()
    if response_from_models['status']:
        request.session['shows'] = response_from_models['shows']
        request.session['status'] = True
    else:
        request.session['errors'] = response_from_models['errors']
        request.session['status'] = False
    return render(request, 'all_shows.html')

# Select Show To Remove
def select_show_to_delete(request):
    response_from_models = Show.shows.get_all_shows()
    if response_from_models['status']:
        request.session['errors'] = ""
        request.session['shows'] = response_from_models['shows']
        request.session['status'] = True
    else:
        request.session['errors'] = response_from_models['errors']
        request.session['status'] = False
    return render(request, 'remove_show.html')

# Delete Show Route
def remove_show(request):
    response_from_models = Show.shows.delete_show(request.POST['show_id'])
    if response_from_models['status']:
        request.session['status'] = True
        return get_all_shows(request)
    else:
        request.session['status'] = False
        request.session['errors'] = response_from_models['errors']
        return render(request, 'remove_show.html')
    
#-----------------------------------#
#----- Internal Helper Methods -----#
#-----------------------------------#
def delete_session(request):
    request.session['errors'] = []
    request.session['tour_added_bool'] = False
    request.session['tours'] = {}
    request.session['shows'] = {}
