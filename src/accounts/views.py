from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View
from .forms import RegisterForm, LoginForm, ResetPasswordForm, ForgotPasswordForm
from .models import User
from .utils import account_activation_token, send_mail


class RedirectRegisterView(View):
    def get(self, request, *args, **kwargs):
        return redirect('accounts:register')


class RegisterView(TemplateView):
    template_name = 'accounts/register.html'

    def get(self, request, *args, **kwargs):
        return render(request=request, template_name=self.template_name)

    def post(self, request, *args, **kwargs):
        response = {}
        form = RegisterForm(request.POST)
        if not form.is_valid():
            response['status'] = False
            response['error'] = form.errors
            return JsonResponse(response)
        else:
            user = form.save(commit=False)
            user.verification_code = account_activation_token.make_token(user=user)
            pwd = user.password
            user.set_password(pwd)
            user.save()

            mail_sent = send_mail(user=user, request=request)

            if mail_sent:
                response['message'] = 'User Registered Successfully'
            else:
                response['message'] = 'User Registered Successfully'
            response['status'] = True
            return JsonResponse(response)


class LoginView(TemplateView):
    template_name = 'accounts/login.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            return render(request=request, template_name=self.template_name)
        else:
            return redirect('home:indexView')

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        response = {}
        if not form.is_valid():
            response['status'] = False
            response['error'] = form.errors
            return JsonResponse(response)

        email = form.cleaned_data['login_email']
        password = form.cleaned_data['login_password']
        user = authenticate(request=request, email=email, password=password)

        if user is None:
            try:
                user = User.objects.get(email=email)
                if not user.is_active:
                    form.add_error('login_email', 'Email address not verified.')
                else:
                    if user.password != password:
                        form.add_error('login_password', 'Email address and password does not match.')
            except User.DoesNotExist:
                form.add_error('login_email', 'Email address not registered.')

            response['status'] = False
            response['error'] = form.errors
            return JsonResponse(response)

        else:
            login(request, user)
            response = {
                'status': True,
                'message': 'Logging In',
                'redirect_url': settings.LOGIN_REDIRECT_URL,
            }
            return JsonResponse(response)


class ForgotPasswordView(TemplateView):
    form = ForgotPasswordForm()
    template_name = 'accounts/login.html'

    def get(self, request, *args, **kwargs):
        return render(request=request, template_name=self.template_name)


class ResetPassWordView(TemplateView):
    form = ResetPasswordForm()
    template_name = 'accounts/login.html'

    def get(self, request, *args, **kwargs):
        return render(request=request, template_name=self.template_name)


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('home:indexView')



class VerificationView(View):
    template_name = 'accounts/login.html'

    def get(self, request, *args, **kwargs):
        token = kwargs['token']
        email = kwargs['email']
        try:
            user = User.objects.get(email=email, verification_code=token)
            user.is_active = True
            user.save()
            return redirect('accounts:login')

        except User.DoesNotExist:
            return redirect('accounts:register')
