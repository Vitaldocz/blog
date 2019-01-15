from django import forms
from fields import forms as fields
from .models import User


class RegisterForm(forms.ModelForm):
    first_name = fields.char_field('first_name')
    last_name = fields.char_field('last_name')
    email = fields.email_field()
    mobile = fields.mobile_field()
    password = fields.password_field()

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'password',
            'mobile'
        ]


class LoginForm(forms.Form):
    login_email = fields.email_field()
    login_password = fields.password_field()


class ForgotPasswordForm(forms.Form):
    fp_email = fields.email_field()


class ResetPasswordForm(forms.Form):
    password = fields.password_field()
    re_password = fields.password_field(default='Re-type password')
