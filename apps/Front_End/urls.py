from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('tours', views.tours_page, name='tours_page'),
    path('music', views.music_page, name='music_page'),
    path('contact', views.contact_page, name='contact_page'),
    path('store', views.store_page, name='store_page'),
    path('contact', views.contact_page, name='contact_page'),
    path('about', views.about_page, name='about_page'),
]
