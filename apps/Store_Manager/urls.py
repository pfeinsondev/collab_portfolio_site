from django.urls import path
from . import views

urlpatterns = [
    # Get All items
    path('get_all_items', views.get_all_items, name='get_all_items'),
    # Add item
    path('get_item_info', views.get_item_info, name='get_item_info'),
    path('process_item_info', views.process_item_info, name='process_item_info'),
    # Delete Item
    path('select_item_to_delete', views.select_item_to_delete, name='select_item_to_delete'),
    path('delete_item', views.delete_item, name='delete_item')
]
