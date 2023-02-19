from django.urls import path
from . import views
 
urlpatterns = [
    path('', views.home_view),
    path('callback', views.callback, name="callback"),
    path('push_morning_message', views.push_morning_message, name='push_morning_message'),
    path('remind_reverve_movie_ticket', views.remind_reverve_movie_ticket, name='remind_reverve_movie_ticket')
]