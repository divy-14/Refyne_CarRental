from rest_framework import serializers
from .models import Car, NewUser, BookedCars


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


class BookCarSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookedCars
        fields = ["userid", "toDate", "fromDate", "carLicenseNumber"]
