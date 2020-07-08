from django.shortcuts import render
from ..Music_Manager.models import Album, Song
from ..Tour_Manager.models import Tour
from ..Store_Manager.models import Store
from .models import AboutInformation, AboutInformationManager
from ..NewsFeed_Manager.models import NewsFeed

# Home Page
def home_page(request):
    response_from_models = NewsFeed.newsfeed_manager.get_all_entries()
    if response_from_models['status']:
        request.session['status'] = True
        request.session['all_posts'] = response_from_models['entries_list_json']
    else:
        response_from_models['status'] = False
        request.session['errors'] = "Sorry! Something went wrong and this page is no longer available. You should find the other links still work"
    return render(request, 'home.html')

# Music page
def music_page(request):
    response_from_models = Song.songs.get_all_music_as_json()
    if response_from_models['status']:
        request.session['all_music'] = response_from_models['all_music']
        request.session['status'] = True
    else:
        request.session['status'] = False
    return render(request, 'music.html')
    
# Tours Page
def tours_page(request):
    response_from_models = Tour.tours.get_all_tours()
    if response_from_models['status']:
        request.session['tours'] = response_from_models['tours']
        request.session['status'] = True
    else:
        request.session['errors'] = response_from_models['errors']
        request.session['status'] = False
    return render(request, 'tours.html')

# Store Page
def store_page(request):
    response_from_models = Store.stores.get_all_items()
    if response_from_models['status']:
        request.session['status'] = True
        request.session['all_items'] = response_from_models['all_items']
    else:
        request.session['status'] = False
        request.session['errors'] = response_from_models['errors']
    return render(request, 'store.html')

# Contact Page
def contact_page(request):
    return render(request, 'contact.html')

# About Page
def about_page(request):
    response_from_models = AboutInformation.about_me_manager.get_about_me_information()
    if response_from_models['status']:
        request.session['status'] = True
        request.session['about_me_image'] = response_from_models['current_information']['about_me_image'].url
        request.session['about_me_text'] = response_from_models['current_information']['about_me_text']
    else:
        request.session['status'] = False
        request.session['errors'] = response_from_models['errors']
    return render(request, 'about.html')
