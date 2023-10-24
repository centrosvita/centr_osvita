# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.HomePageView.as_view(), name='home'),
    url(r'^robots.txt/$', views.RobotsTxtView.as_view()),
    url(r'^teachers/$', views.OurTeachersView.as_view(), name='teachers'),
    url(r'^statistics/$', views.StatisticsView.as_view(), name='statistics'),
    url(r'^math/$', views.MathView.as_view(), name='math'),
    url(r'^ukrainian/$', views.UkrainianView.as_view(), name='ukrainian'),
    url(r'^english/$', views.EnglishView.as_view(), name='english'),
    url(r'^history/$', views.HistoryView.as_view(), name='history'),
    url(r'^physics/$', views.PhysicsView.as_view(), name='physics'),
    url(r'^geography/$', views.GeographyView.as_view(), name='geography'),
    url(r'^biology/$', views.BiologyView.as_view(), name='biology'),
    url(r'^chemistry/$', views.ChemistryView.as_view(), name='chemistry'),
]
