from django.forms import ValidationError


def check_mobile_length(mobile):
    if len(str(mobile)) == 10:
        return True
    raise ValidationError('Please Enter a valid 10 digit mobile number.')
