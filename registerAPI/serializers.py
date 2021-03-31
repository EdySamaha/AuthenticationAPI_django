from rest_framework import serializers
from .models import Account

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model=Account
        fields='__all__'

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model=Account
        # fields='__all__' #maybe more secure
        fields = ['username', 'email','password']

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model=Account
        fields = ['email','password']
