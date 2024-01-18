from django.urls import path
from .views import home, room, room_add, update_room, delete_room

#now import the views.py file into this code
urlpatterns=[
  path('',home, name= "home"),
  path('room/delete/<str:pk>', delete_room, name="delete_room"),
  path('room/update/<str:pk>', update_room, name="update_room"),
  path('room/add', room_add, name="room_add"),
  path('room/<str:pk>', room, name="room"),

]