from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('register', views.register),
    path('dashboard', views.dashboard),
    path('logout', views.logout),
    path('login_user', views.login),
]
