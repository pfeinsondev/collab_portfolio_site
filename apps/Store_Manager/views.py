from django.shortcuts import render, redirect
from ..Store_Manager.models import Store

#---------------------#
#--- Get All Items ---#
#---------------------#
def get_all_items(request):
    response_from_models = Store.stores.get_all_items()
    if response_from_models['status']:
        request.session['status'] = True
        request.session['all_items'] = response_from_models['all_items']
    else:
        request.session['status'] = False
        request.session['errors'] = response_from_models['errors']
    return render(request, 'all_items.html')


#----------------#
#--- Add item ---#
#----------------#

def get_item_info(request):
    request.session['status'] = True
    return render(request, 'get_item_info.html')

def process_item_info(request):
    response_from_models = Store.stores.add_item(request.POST, request.FILES)
    if not response_from_models['status']:
        request.session['errors'] = response_from_models['errors']
        request.session['status'] = False
        return render(request, 'get_item_info.html')
    else:
        request.session['status'] = True
        return get_all_items(request)


#-------------------#
#--- Remove Item ---#
#-------------------#

def select_item_to_delete(request):
    request.session['item_deleted_bool'] = False
    response_from_models = Store.stores.get_all_item_names()
    if response_from_models['status']:
        request.session['all_item_names'] = response_from_models['all_item_names']
        request.session['status'] = True
    else:
        request.session['status'] = False
        request.session['errors'] = response_from_models['errors']
    return render(request, 'select_item_to_delete.html')

def delete_item(request):
    response_from_models = Store.stores.delete_item(request.POST['item_name_to_delete'])
    if response_from_models['status']:
        response_from_models = Store.stores.get_all_item_names()
        if response_from_models['status']:
            request.session['all_item_names'] = response_from_models['all_item_names']
            request.session['status'] = True
            return render(request, 'select_item_to_delete.html')
        else:
            request.session['errors'] = response_from_models['errors']
            request.session['status'] = False
            return render(request, 'select_item_to_delete.html')
    else:
        request.session['item_deleted_bool'] = False
        return render(request, 'select_item_to_delete.html')
