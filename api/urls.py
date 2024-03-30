from django.urls import path
from . import views

urlpatterns = [
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('client', views.ClientGetPost.as_view(), name='client_register'),
]