# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from django.contrib.auth import logout, login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import View

from centr_osvita.profiles.forms import ProfileRegisterForm
from centr_osvita.users.forms import UserRegisterForm


class RegisterView(View):
    template_name = 'auth/register.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('common:home')
        return render(request, self.template_name, {'user_form': UserRegisterForm, 'profile_form': ProfileRegisterForm})

    def post(self, request, *args, **kwargs):
        user_form = UserRegisterForm(data=request.POST)
        profile_form = ProfileRegisterForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile_form.user = user
            profile_form.save()
            login(request, user)
            return redirect(reverse('common:home') + '#subjects')

        return render(request, self.template_name, {'user_form': user_form, 'profile_form': profile_form})


class LoginView(View):
    template_name = 'auth/login.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('common:home')
        return render(request, self.template_name, {'form': AuthenticationForm})

    def post(self, request, *args, **kwargs):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(reverse('common:home') + '#subjects')
        else:
            return render(request, self.template_name, {'form': form})


def logout_view(request):
    logout(request)
    response = redirect('common:home')
    return response
