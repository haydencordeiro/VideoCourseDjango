from django.urls import path
from . import views
urlpatterns = [
    path('videos', views.VideosPage, name='videos'),
    path('', views.home, name='home'),
    path("logout", views.logout_request, name="logout"),
    path("login", views.LoginView, name="LoginView"),
    path("register", views.RegisterView, name="RegisterView"),
    path("checkout/<int:id>/", views.checkout, name="Checkout"),
    path("handlerequest/", views.handlerequest, name="HandleRequest"),
    path('dashboard/', views.AdminHome, name='AdminHome'),
    path('addvideos/', views.AddVideo, name='AddVideo'),
    path('deletevideos/<int:id>/', views.DeleteVideo, name='DeleteVideo'),
    path('addtestimonial/', views.AddTestimonial, name='AddTestimonial'),
    path('deletetestimonial/<int:id>/',
         views.DeleteTestimonial, name='DeleteTestimonial'),
    path('subtype/', views.AddSubType, name='AddSubType'),
    path('deletesubtype/<int:id>/',
         views.DeleteSubType, name='DeleteSubType'),
    path('editsubtype/<int:id>/',
         views.EditSubType, name='EditSubType'),
    path('addtypeaccess/', views.AddTypeAccess, name='AddTypeAccess'),
    path('deletetypeaccess/<int:id>/',
         views.DeleteTypeAccess, name='DeleteTypeAccess'),







]
