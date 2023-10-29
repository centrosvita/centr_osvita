from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return ['common:home', 'common:teachers', 'common:math', 'common:ukrainian', 'common:english',
                'common:history', 'common:physics', 'common:geography', 'common:biology', 'common:chemistry',
                'blog:blogs']

    def location(self, item):
        return reverse(item)
