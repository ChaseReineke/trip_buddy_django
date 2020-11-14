from django.urls import path     
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('success', views.success),
    path('login', views.login),
    path('trips/new', views.new),
    path('create', views.create),
    path('trips/view/<int:id>', views.view),
    path('trips/edit/<int:id>', views.edit),
    path('trips/edit_trip/<int:id>', views.edit_trip),
    path('trips/delete/<int:id>', views.delete),
    path('trips/join_trip/<int:id>', views.join),
    path('trips/cancel/<int:id>', views.cancel_join),
    path('logout', views.logout),
]