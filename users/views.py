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
from rest_framework.authtoken.models import Token


def signup(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to a success page.
            return redirect('registration_success')
    else:
        form = RegistrationForm()
    return render(request, 'signup.html', {'form': form})

    

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
            'username': user.username
        }, status=status.HTTP_200_OK)