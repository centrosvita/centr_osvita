# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.PostsListView.as_view(), name='blogs'),
    # url(r'^chemistry/$', views.ChemistryView.as_view(), name='chemistry'),
]
