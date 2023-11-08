from django import forms
from django.forms import BaseFormSet
from django.utils.translation import ugettext as _
from model_utils.choices import Choices

from centr_osvita.quiz.models import CommonAnswer, OrderAnswer


class AnswerValidatedFormSet(BaseFormSet):
    def clean(self):
        if any(self.errors):
            return
        key_list = [form.cleaned_data['position'] for form in self.forms]
        if len(set(key_list)) != len(self.forms):
            raise forms.ValidationError(_('You should enter different values'))


class MappingAnswerForm(forms.Form):
    def __init__(self, answer_number, *args, **kwargs):
        super().__init__(*args, **kwargs)
        form_choices = Choices(*CommonAnswer.ORDER_COMMON._triples[:answer_number])
        self.fields['position'] = forms.ChoiceField(
            choices=form_choices,
            widget=forms.RadioSelect(),
            initial=CommonAnswer.ORDER_COMMON.first
        )


class OrderAnswerForm(forms.Form):
    position = forms.ChoiceField(choices=OrderAnswer.ORDER_SECOND_CHAIN,
                                 initial=OrderAnswer.ORDER_SECOND_CHAIN.first, widget=forms.RadioSelect())


class CommonAnswerForm(forms.Form):
    def __init__(self, answer_number, *args, **kwargs):
        super().__init__(*args, **kwargs)
        form_choices = Choices(*CommonAnswer.ORDER_COMMON._triples[:answer_number])
        self.fields['position'] = forms.ChoiceField(
            choices=form_choices,
            widget=forms.RadioSelect(),
            initial=CommonAnswer.ORDER_COMMON.first
        )
