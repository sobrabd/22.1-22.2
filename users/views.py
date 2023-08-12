from django.shortcuts import render
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .models import User
from .forms import UserRegisterForm
from django.core.mail import send_mail
from django.conf import settings


class LoginView(BaseLoginView):
    template_name = 'users/login.html'


class LogoutView(BaseLogoutView):
    pass


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/register.html'

    def form_valid(self, form):
        new_user = form.save()
        # send_mail(
        #     subject='Поздравляем в регистрацией',
        #     message='Вы зарегистрировались на нашей платформе, добро пожаловать!',
        #     from_email=settings.EMAIL_HOST_USER,
        #     recipient_list=[new_user.email]
        # )
        return super().form_valid(form)
