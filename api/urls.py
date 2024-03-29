from django.urls import path
from . import views

urlpatterns = [
    path('client', views.ClientGetPost.as_view(), name='client_register'),
]