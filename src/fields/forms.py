from django import forms
from .validators import check_mobile_length
from .utils import emailRegex, mobileRegex, textRegex, to_upper_case_string


def char_field(name):
    return forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': to_upper_case_string(name),
        'pattern': textRegex,
        'required': True,
        'autocomplete': 'On'
    }))


def email_field():
    return forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': to_upper_case_string('email_address'),
        'pattern': emailRegex,
        'required': True,
        'autocomplete': 'On'
    }))


def password_field(default=None):
    if default is None:
        default = 'password'
    return forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': to_upper_case_string(default),
        'required': True,
        'autocomplete': 'Off'
    }))


def mobile_field():
    return forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'placeholder': to_upper_case_string('mobile_number'),
            'pattern': mobileRegex,
            'required': True,
            'autocomplete': 'On'
        }),
        validators=[check_mobile_length]
    )


def hidden_field():
    return forms.CharField(widget=forms.HiddenInput(attrs={
        'required': True,
        'disabled': True,
        'autocomplete': True,
    }))
