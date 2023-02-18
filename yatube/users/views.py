from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth.views import PasswordResetDoneView
from django.contrib.auth.views import PasswordResetCompleteView
from django.contrib.auth.views import PasswordChangeDoneView
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy

from .forms import CreationForm


class SignUp(CreateView):
    form_class = CreationForm
    template_name = 'users/signup.html'
    success_url = reverse_lazy('posts:index')


class Login(LoginView):
    success_url = reverse_lazy('users:login')
    template_name = 'users/login.html'


class Logout(LogoutView):
    success_url = reverse_lazy('users:logout')
    template_name = 'users/logged_out.html'


class PasswordChange(PasswordChangeView):
    success_url = reverse_lazy('users:password_change_form')
    template_name = 'users/password_change_form.html'


class PasswordChangeDone(PasswordChangeDoneView):
    success_url = reverse_lazy('users:password_change_done')
    template_name = 'users/password_change_done.html'


class PasswordReset(PasswordResetView):
    success_url = reverse_lazy('users:password_reset')
    template_name = 'users/password_reset_form.html'


class PasswordResetDone(PasswordResetDoneView):
    success_url = reverse_lazy('users:password_reset_done')
    template_name = 'users/password_reset_done.html'


class PasswordResetConfirm(PasswordResetConfirmView):
    success_url = reverse_lazy('users:password_reset_confirm')
    template_name = 'users/password_reset_confirm.html'


class PasswordResetComplete(PasswordResetCompleteView):
    success_url = reverse_lazy('userspassword_reset_complete')
    template_name = 'users/password_reset_complete.html'
