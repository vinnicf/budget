from allauth.account.forms import ResetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from dj_rest_auth.serializers import PasswordResetSerializer
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from allauth.account.utils import user_pk_to_url_str
from allauth.account.adapter import get_adapter
from allauth.utils import build_absolute_uri


def int_to_base36(num):
    """Converts an integer to a base36 string."""
    alphabet = '0123456789abcdefghijklmnopqrstuvwxyz'
    if num < 0:
        return '-' + int_to_base36(-num)
    base36 = ''
    while num != 0:
        num, i = divmod(num, 36)
        base36 = alphabet[i] + base36
    return base36 or alphabet[0]


class CustomAllAuthPasswordResetForm(ResetPasswordForm):
    def save(self, request, **kwargs):
        # Extracts the domain we are on
        current_site = get_current_site(request)
        email = self.cleaned_data["email"]

        for user in self.users:
            temp_key = default_token_generator.make_token(user)

            uid = int_to_base36(user.id)

            # Construct the path to  password reset page in  frontend
            path = f'http://127.0.0.1:8000/usuario/recuperar-senha/{uid}/{temp_key}'
            url = build_absolute_uri(request, path)

            context = {
                'current_site': current_site,
                'user': user,
                'password_reset_url': url,
                'request': request,
            }

            # Send the email to the user with the custom password reset link
            get_adapter(request).send_mail(
                'account/email/password_reset_key',
                email,
                context
            )
        return self.cleaned_data["email"]

class CustomPasswordResetSerializer(PasswordResetSerializer):
    @property
    def password_reset_form_class(self):
        return CustomAllAuthPasswordResetForm

    def save(self):
        request = self.context.get('request')

        #Set some values to grigger send_email method
        opts = {
            'use_https': request.is_secure(),
            'from_email': getattr(settings, 'DEFAULT_FROM_EMAIL'),
            'request': request,
            'token_generator': default_token_generator,
        }

        opts.update(self.get_email_options())
        self.reset_form.save(**opts)
