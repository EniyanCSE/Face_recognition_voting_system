from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('visualize/', views.index, name='index'),  # URL pattern should be 'visualize/'
    path('visualize/login_po/', views.login, name='login'),
    path('visualize/panel_po/', views.panel, name='panel'),
    # path('visualize/panel_po/', login_required(views.panel), name='panel'),  # Use login_required decorator
    path('visualize/add_user/', views.add_user, name='add_user'),
    path('show_results/', views.show_results, name='show_results'),
    path('visualize/reset_votes/', views.reset_votes, name='reset_votes'),
    path('increase_vote/', views.increase_vote, name='increase_vote'),
    path('visualize/vote_panel/', views.vote_panel, name='vote_panel'),  
    path('visualize/register_user/', views.register_user, name='register_user'),
    path('visualize/user_login/', views.user_login, name='user_login'),
]

