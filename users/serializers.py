from django.contrib.auth import authenticate
from rest_framework import serializers
from allauth.account.models import EmailAddress

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            # Check if the user's email is verified
            if not EmailAddress.objects.filter(user=user, verified=True).exists():
                raise serializers.ValidationError("Your email address is not verified.")
            return user
        raise serializers.ValidationError("Incorrect Credentials")