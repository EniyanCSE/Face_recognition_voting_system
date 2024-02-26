from django.contrib import admin
from django.urls import path, include  # Include the 'include' function
from voting_web.views import home_view  
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', home_view, name='home'),
    path('admin/', admin.site.urls),
    path('myapp/', include('voting_web.urls')), # Include the app's URLs without a namespace
    
]
