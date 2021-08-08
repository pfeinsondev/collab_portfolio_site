from django.conf import settings
from django.urls import path, include
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns = [ 
    path('', include('apps.Admin_Manager.urls')),
    path('', include('apps.Tour_Manager.urls')),
    path('', include('apps.Music_Manager.urls')),
    path('', include('apps.Store_Manager.urls')),
    path('', include('apps.Front_End.urls')),
    path('', include('apps.NewsFeed_Manager.urls')),
    path('', include('apps.Art_Manager.urls'))
    #url(r'collect_new_admin_data', apps.Admin_Manager.views.collect_new_admin_data),
    #url(r'login_admin', apps.Admin_Manager.views.admin_login)
]

# Enables Uploads
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


