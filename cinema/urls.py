from django.urls import path
from . import views
urlpatterns = [
 path('', views.index, name='index'),
 path('manage/', views.manage, name='manage'),
 path('manage/create-cinema/', views.create_cinema, name='create-cinema'),
 path('manage/add-film/', views.add_film, name='add-film'),
 path('manage/add-time-frame/', views.add_time_frame, name='add-time-frame'),
 path('manage/add-cinema-hall/', views.add_cinema_hall, name='add-cinema-hall'),
 path('manage/add-schedule/', views.add_schedule, name='add-schedule'),
 path('manage/edit-schedule/', views.edit_schedule, name='edit-schedule'),
 path('manage/get-halls-by-cinema/', views.get_halls_by_cinema, name='get-halls-by-cinema'),
 path('find-shows/', views.find_shows, name='find-shows'),
 path('book-ticket/', views.book_ticket, name='book-ticket'),
]