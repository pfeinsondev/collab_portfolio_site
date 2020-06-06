from django.shortcuts import render
from ..NewsFeed_Manager.models import NewsFeed, NewsFeed_Manager

#---------------#
#   All posts   #
#---------------#
def get_all_newsfeed_entries(request):
    response_from_models = NewsFeed.newsfeed_manager.get_all_entries()
    if response_from_models['status']:
        request.session['entries_list_json'] = response_from_models['entries_list_json']
        request.session['status'] = True
    else:
        request.session['status'] = False
        request.session['errors'] = response_from_models['errors']
    return render(request, 'all_newsfeed_entries.html')


#-------------------#
#   New Post Form   #
#-------------------#
def collect_new_entry_data(request):
    return render(request, 'collect_new_entry_data.html')

#---------------------------#
#   Process New Post Data   #
#---------------------------#
def process_new_entry_data(request):
    response_from_models = NewsFeed.newsfeed_manager.create_new_entry(request.FILES)
    if not response_from_models['status']:
        request.session['status'] = False
        request.session['errors'] = response_from_models['errors']
        return collect_new_entry_data(request)
    else:
        request.session['status'] = True
        return get_all_newsfeed_entries(request)

#----------------------#
#   Delete Post Form   #
#----------------------#
def select_post_to_delete(request):
    response_from_models = NewsFeed.newsfeed_manager.get_all_entries()
    if response_from_models['status']:
        request.session['status'] = True
        request.session['entries_list_json']
    else:
        request.session['status'] = False
        request.session['errors'] = "No Posts Found!"
    return render(request, 'select_post_to_delete.html')

#-----------------#
#   Delete Post   #
#-----------------#
def delete_post(request):
    response_from_models = NewsFeed.newsfeed_manager.delete_entry(request.POST)
    if response_from_models['status']:
        request.session['status'] = True
        return get_all_newsfeed_entries(request)
    else:
        request.session['status'] = False
        request.session['errors'] = response_from_models['errors']
        return render(request, 'select_post_to_delete.html')
    
