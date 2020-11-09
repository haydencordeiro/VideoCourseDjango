from django.urls import path
from . import views
urlpatterns = [
    path('videos', views.VideosPage, name='videos'),
    path('', views.home, name='home'),
    path("logout", views.logout_request, name="logout"),
]
