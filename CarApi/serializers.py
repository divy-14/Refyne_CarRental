from rest_framework import serializers
from .models import Car, NewUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewUser
        fields = ["userName", "userMobile"]


class CarSerializer(serializers.ModelSerializer):
    # userMobile = serializers.ReadOnlyField()
    class Meta:
        model = Car
        fields = ["carLicenseNumber", "Manufacturer",
                  "Model", "base_price", "pph", "security_deposit"]
