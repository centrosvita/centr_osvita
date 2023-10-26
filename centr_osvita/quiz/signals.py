import os
from django.db import models
from django.dispatch import receiver
from centr_osvita.quiz.models import Question


@receiver(models.signals.post_delete, sender=Question)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `Question` object is deleted.
    """
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)


@receiver(models.signals.pre_save, sender=Question)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `Question` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_image = Question.objects.get(pk=instance.pk).image
    except Question.DoesNotExist:
        return False

    new_image = instance.image
    if not old_image == new_image:
        if old_image and os.path.isfile(old_image.path):
            os.remove(old_image.path)
