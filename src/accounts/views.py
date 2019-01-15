from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View
from .forms import RegisterForm, LoginForm, ResetPasswordForm, ForgotPasswordForm
from .form_response import error_response, success_response
from .models import User
from .utils import (
    account_activation_token,
    send_account_activation_mail,
    send_password_reset_mail,
    password_reset_token,
)


class ForgotPasswordView(TemplateView):
    def get(self, request, *args, **kwargs):
        template_name = 'accounts/forgot_pass.html'
        return render(request=request, template_name=template_name)

    def post(self, request, *args, **kwargs):
        form = ForgotPasswordForm(request.POST)
        if not form.is_valid():
            response = error_response(error=form.errors)
            return JsonResponse(response.to_json(), safe=False)

        user = User.get_user_by_email(email=form.cleaned_data['fp_email'])
        if user is None:
            form.add_error('fp_email', 'Email address not registered.')
            response = error_response(error=form.errors)

        else:
            token = password_reset_token.make_token(user=user)
            uidb64 = user.get_uidb64()

            mail_sent = send_password_reset_mail(request, user, uidb64, token)

            if mail_sent:
                response = success_response(message='Password reset link has been mailed to you.')
            else:
                form.add_error('fp_email', 'Could not send password reset link to your mail. Please try again later.')
                response = error_response(error=form.errors)
        return JsonResponse(response.to_json(), safe=False)


class LoginView(TemplateView):
    def get(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            template_name = 'accounts/login.html'
            return render(request=request, template_name=template_name)
        else:
            return redirect('home:indexView')

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if not form.is_valid():
            response = error_response(error=form.errors)
            return JsonResponse(response.to_json(), safe=False)

        email = form.cleaned_data['login_email']
        password = form.cleaned_data['login_password']
        user = authenticate(request=request, email=email, password=password)

        if user is None:
            user = User.get_user_by_email(email=email)
            if user:
                if user.check_active():
                    form.add_error('login_password', 'Email address and password does not match.')
                else:
                    form.add_error('login_email', 'Email address not verified.')
            else:
                form.add_error('login_email', 'Email address not registered.')

            response = error_response(error=form.errors)
            return JsonResponse(response.to_json(), safe=False)

        else:
            login(request, user)
            try:
                redirect_url = request.POST['next']
            except KeyError:
                redirect_url = settings.LOGIN_REDIRECT_URL

            response = success_response(message='Logging In', redirect_url=redirect_url)
            return JsonResponse(response.to_json(), safe=False)


class LogoutView(View):

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('home:indexView')


class RedirectRegisterView(View):
    def get(self, request, *args, **kwargs):
        return redirect('accounts:register')


class RegisterView(TemplateView):
    def get(self, request, *args, **kwargs):
        template_name = 'accounts/register.html'
        return render(request=request, template_name=template_name)

    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST)
        if not form.is_valid():
            response = error_response(error=form.errors)

        else:
            user = form.save(commit=False)
            user.verification_code = account_activation_token.make_token(user=user)
            pwd = user.password
            user.set_password(pwd)
            user.save()

            mail_sent = send_account_activation_mail(user=user, request=request)

            if not mail_sent:
                user.is_active = True
                user.save()

            response = success_response(message='User Registered Successfully')
        return JsonResponse(response.to_json(), safe=False)


class ResetPasswordView(TemplateView):
    template_name = 'accounts/reset_pass.html'

    def get(self, request, *args, **kwargs):
        uidb64 = kwargs['uidb64']
        token = kwargs['token']
        context = {
            'uidb64': uidb64,
            'token': token,
            'reset_password_form': ResetPasswordForm()
        }

        try:
            user = User.get_user_by_uidb64(uidb64=uidb64)
            if user is None:
                return render(request, template_name='home/broken_link.html')
            elif password_reset_token.check_token(user, token):
                context['username'] = user.get_full_name()
                return render(request=request, template_name=self.template_name, context=context)
            else:
                return render(request, template_name='home/broken_link.html')

        except ValueError:
            return render(request, template_name='home/broken_link.html')

    def post(self, request, *args, **kwargs):
        form = ResetPasswordForm(request.POST)

        if not form.is_valid():
            response = error_response(error=form.errors)
            return JsonResponse(response.to_json())

        if form.cleaned_data['password'] != form.cleaned_data['re_password']:
            form.add_error('re_password', 'Passwords does not match.')
            response = error_response(error=form.errors)
            return JsonResponse(response.to_json())

        user = User.get_user_by_uidb64(uidb64=kwargs['uidb64'])
        user.set_password(raw_password=form.cleaned_data['password'])
        user.save()
        response = success_response(message='Password Changed Successfully.')
        return JsonResponse(response.to_json())


class VerificationView(View):
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
