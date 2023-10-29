from django.contrib.sitemaps import Sitemap
from centr_osvita.blogs.models import Post


class PostSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Post.objects.filter(publish=True)

    def lastmod(self, obj):
        return obj.modified

    def location(self, obj):
        return '/blog/{0}'.format(obj.slug)
