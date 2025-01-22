from django.urls import path
from .views import home, user_login, logout_view, get_user_geojson, my_profile, edit_profile, save_geojson


urlpatterns = [
    path('login/', user_login, name='login'),
    path('home/', home, name='home'),
    path('logout/', logout_view, name='logout'),
    path('user-geojson/', get_user_geojson, name='user_geojson'),
    path('myprofile/', my_profile, name='myprofile'),
    path('editprofile/', edit_profile, name='editprofile'),
    path('save-geojson/', save_geojson, name='save_geojson'),
  
]