from django.conf.urls import url
from . import views

urlpatterns = [
    #rendering routes
    url(r'^$', views.index),
    url(r'^quotes$', views.quotes),
    url(r'^users/(?P<number>\d+)$', views.users),

    #post routes
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^register$', views.register),
    url(r'^add$', views.add),
    url(r'^favorite/(?P<number>\d+)$', views.favorite),
    url(r'^remove/(?P<number>\d+)$', views.remove),
]