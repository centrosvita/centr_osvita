# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    url(settings.ADMIN_URL, include(admin.site.urls)),
    url(r'^', include("centr_osvita.common.urls", namespace="common")),
    url(r'^users/', include("centr_osvita.users.urls", namespace="users")),
    url(r'^quiz/', include("centr_osvita.quiz.urls", namespace="quiz")),
    url(r'^blog/', include("centr_osvita.blogs.urls", namespace="blog")),
]

if settings.USE_SILK:
    urlpatterns += [
        url(r'^silk/', include('silk.urls', namespace='silk'))
    ]

if settings.USE_DEBUG_TOOLBAR:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
