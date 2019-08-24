# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views

urlpatterns = [

    # The home page
    url(r'fetchnumber$', views.fetchNumber, name='fetchnumber'),
    url(r'analysis$', views.analysis, name='analysis'),
    url(r'getanalysis$', views.getanalysis, name='getanalysis'),
    url(r'export$', views.export, name='export'),

    url(r'^$', views.index, name='index'),
]

