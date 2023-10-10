from django.db import models
from django.utils.translation import ugettext_lazy as _
import time


def post_image_path(instance, filename):
    dot_position = filename.find('.')
    return 'posts/{0}'.format(filename[:dot_position]+str(int(time.time()))+filename[dot_position:])


class Post(models.Model):
    title = models.CharField(_("Title"), max_length=255)
    content = models.TextField(_("Content"))
    slug = models.SlugField(_("Article url"))
    image = models.ImageField(_("Image"), upload_to=post_image_path)
    publish = models.BooleanField(_("Publish"), default=True)
