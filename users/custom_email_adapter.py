from allauth.account.adapter import DefaultAccountAdapter
from django.contrib.auth.tokens import default_token_generator

class CustomEmailAdapter(DefaultAccountAdapter):

    def send_mail(self, template_prefix, email, context):
        # Check if the email is for password reset
        if template_prefix == "account/email/password_reset_key":
            context['uid'] = context['user'].pk
            context['token'] = default_token_generator.make_token(context['user'])
        return super(CustomEmailAdapter, self).send_mail(template_prefix, email, context)
