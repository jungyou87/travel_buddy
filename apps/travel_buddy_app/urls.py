from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^main$', views.main),

    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),

    url(r'^travels$', views.travels),
    url(r'^travels/add$', views.travels_add),
    url(r'^travels/add_trip$', views.add_trip),

    url(r'^travels/destination/(?P<id>\d+)$', views.destination),

    url(r'^travels/destination/(?P<id>\d+)/join$', views.destination_join),


]
