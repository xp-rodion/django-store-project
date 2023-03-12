from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView

from common.views import TitleMixin
from users.forms import UserLoginForm, UserProfileForm, UserRegisterForm
from users.models import EmailVerification, User


class UserLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm


class UserRegistrateView(TitleMixin, SuccessMessageMixin, CreateView):
    model = User
    template_name = 'users/register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy("users:login")
    success_message = f'Вы успешно зарегистрированы!'
    title = "Store - Регистрация"


class UserProfileView(TitleMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    success_url = 'users:profile'
    title = 'Store - Личный кабинет'

    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.object.id, ))


class EmailVerificationView(TitleMixin, TemplateView):
    title = 'Store - Подтверждение электронной почты'
    template_name = 'users/email_verification.html'

    def get(self, request, *args, **kwargs):
        code = kwargs.get('code')
        user = User.objects.get(email=kwargs.get('email'))
        email_verifications = EmailVerification.objects.filter(user=user, code=code)
        if email_verifications.exists() and email_verifications.first().is_expired():
            user.is_verified_email = True
            user.save()
            return super(EmailVerificationView, self).get(request, *args, **kwargs)
        return HttpResponseRedirect(reverse('index'))
