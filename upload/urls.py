from django.urls import path     
from . import views

urlpatterns = [
    path('home', views.playsound),
    path('add-cat', views.add_cat),
    path('sounds/<int:id>/destroy', views.delete_entry),
    path('sounds/<int:id>/details', views.details),
    path('sounds/<int:id>/entry_edit', views.entry_edit),
    path('cat/destroy', views.delete_cat),
    path('destroy', views.delete_cat),
    path('upload', views.upload),
    path('sounds/<int:id>/process', views.process),
    path('sounds/<int:id>/edit_cat', views.edit_cat),
    path('sounds/<int:id>/fav',views.add_to_fav),

]