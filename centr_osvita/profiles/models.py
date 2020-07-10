from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel
from phonenumber_field.modelfields import PhoneNumberField
from model_utils.choices import Choices


class Profile(TimeStampedModel):
    GRADE_NUMBER = Choices(
        (9, 'nine', '9'),
        (10, 'ten', '10'),
        (11, 'eleven', '11'),
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name=_('User'), on_delete=models.CASCADE)
    full_name = models.CharField(_('full name'), max_length=255, help_text=_('Maximum length is 255 symbols'))
    parent_full_name = models.CharField(_('Parent fullname'), max_length=255,
                                        help_text=_('Maximum length is 255 symbols'))
    parent_phone = PhoneNumberField(_('Parent phone'))
    institution_name = models.CharField(_('Institution name'), max_length=255,
                                        help_text=_('Maximum length is 255 symbols'))
    grade = models.IntegerField(_("Grade number"), choices=GRADE_NUMBER, null=True, blank=True)

    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')

    def __str__(self):
        return self.full_name
