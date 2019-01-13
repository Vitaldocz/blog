from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils import six


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp)
        )


account_activation_token = AccountActivationTokenGenerator()


def send_mail(request, user):
    current_site = get_current_site(request)
    protocol = request.scheme
    sender = settings.EMAIL_HOST_USER
    subject = '[E-Cell, IIT Kharagpur]: Verification email for participating in GES 2019'
    message = render_to_string('emails/email_verify.html', {
        'user': user,
        'domain': current_site.domain,
        'token': user.verification_code,
        'protocol': protocol
    })

    msg = EmailMessage(subject=subject, body=message, from_email=sender, bcc=[user.email])
    msg.content_subtype = "html"  # Main content is now text/html
    return msg.send()
