from django.urls import path
from authservice import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),

]
# Compare this snippet from authservice/views.py:
