from django.urls import path
from . import views
urlpatterns = [
    path('',views.showing,name='showing'),
    path('movie/',views.index,name='index'),
    path('book/',views.book,name='book'),
]