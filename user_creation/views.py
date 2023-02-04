from django.contrib.auth.forms import AuthenticationForm
from django.utils.decorators import method_decorator
from django.views.generic import FormView

from .forms import SignUpForm
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_protect


@method_decorator(csrf_protect, name='dispatch')
class SignUpView(FormView):
    template_name = 'signup.html'
    form_class = SignUpForm
    success_url = reverse_lazy('manager:tasks')

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data['username']
        password = form.cleaned_data['password1']
        user = authenticate(username=username, password=password)
        auth_login(self.request, user)
        return super().form_valid(form)


@method_decorator(csrf_protect, name='dispatch')
class LoginView(FormView):
    template_name = 'login.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('manager:tasks')

    def form_valid(self, form):
        auth_login(self.request, form.get_user())
        return super().form_valid(form)


class LogoutView(FormView):
    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return redirect('user-creation:login')
