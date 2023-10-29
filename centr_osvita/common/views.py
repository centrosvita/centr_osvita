# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.utils.translation import ugettext as _
from django.views.generic import View
from django.views.generic.base import TemplateView
from django.conf import settings
from django.http.response import HttpResponse
from django.http import Http404
from centr_osvita.quiz.models import Subject


class HealthCheckView(View):

    def get(self, request, *args, **kwargs):
        return HttpResponse(settings.HEALTH_CHECK_BODY, status=200)


class HomePageView(TemplateView):
    template_name = "web/home.html"


class OurTeachersView(TemplateView):
    template_name = "web/ourTeachers.html"


class StatisticsView(View):
    template_name = "web/statistics.html"
    param = None
    subject = None

    def dispatch(self, request, *args, **kwargs):
        param = self.request.GET.get('subject')
        self.subject = Subject.objects.filter(slug=param).first()
        if not self.subject:
            raise Http404(_("Not found"))
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = dict()
        context['subject'] = self.subject
        return render(request, self.template_name, context)


class MathView(TemplateView):
    template_name = "web/math.html"


class UkrainianView(TemplateView):
    template_name = "web/ukrainian.html"


class EnglishView(TemplateView):
    template_name = "web/english.html"


class HistoryView(TemplateView):
    template_name = "web/history.html"


class PhysicsView(TemplateView):
    template_name = "web/physics.html"


class GeographyView(TemplateView):
    template_name = "web/geography.html"


class BiologyView(TemplateView):
    template_name = "web/biology.html"


class ChemistryView(TemplateView):
    template_name = "web/chemistry.html"


class RobotsTxtView(TemplateView):
    template_name = "robots.txt"
    content_type = 'text/plain'
