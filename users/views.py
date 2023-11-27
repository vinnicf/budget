from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from .forms import RegistrationForm, UserModalForm
from .models import CustomUser
from .serializers import LoginSerializer
from bootstrap_modal_forms.generic import BSModalCreateView
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.http import JsonResponse
from rest_framework.authtoken.models import Token
import stripe
from allauth.account.models import EmailAddress
from allauth.account.utils import send_email_confirmation



stripe.api_key = settings.STRIPE_SECRET_KEY


def signup(request):
    upgrade = request.GET.get('upgrade', 'false') == 'true'
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Trigger email confirmation
            email, created = EmailAddress.objects.get_or_create(user=user, email=user.email)
            email.verified = False
            email.set_as_primary()
            email.save()
            send_email_confirmation(request, user, signup=True)

            # Redirect to a success page.
            return redirect('compositions:home')
        else:
            print(form.errors)  # Or log the errors somewhere
    else:
        form = RegistrationForm()
    return render(request, 'signup.html', {'form': form})



def payment_view(request, user_id):
    # Verify the user_id and fetch necessary details based on your application logic

    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price': 'price_1OGhj8IEZ29y0tWF3phxYcxn',  # Your price ID
                'quantity': 1,
            }],
            mode='payment',
            success_url=request.build_absolute_uri('/success/'),  # URL to redirect to on successful payment
            cancel_url=request.build_absolute_uri('/cancel/'),  # URL to redirect to on cancellation
        )

        # Redirect to Stripe Checkout
        return redirect(checkout_session.url)

    except stripe.error.StripeError as e:
        # Handle Stripe errors
        return render(request, 'users/payment_error.html', {'error': str(e)})


class PricingView(TemplateView):
    template_name = 'users/pricing.html'


class UserCreateView(BSModalCreateView):
    template_name = 'modalform.html'
    form_class = UserModalForm
    success_message = 'Sucesso. User Criado'
    success_url = reverse_lazy('home')


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name
        }, status=status.HTTP_200_OK)