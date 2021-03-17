from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from .serializers import CarSerializer, UserSerializer
from .models import Car, NewUser
from rest_framework import status, permissions
from rest_framework.response import Response


class CarApi(APIView):
    '''
    send info of cars over api
    '''

    def get(self, request, format=None):
        cars = Car.objects.all()
        # important to put many=True
        serializer = CarSerializer(cars, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CarSerializer(data=request.data)
        permission_classes = [permissions.AllowAny]

        try:
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(
                    {'id': serializer.data.get('carLicenseNumber')},
                    status=status.HTTP_201_CREATED,
                )
        except:
            return Response(
                {'Bad Request try again, the car with same number plate may already exist'},
                status=status.HTTP_404_NOT_FOUND)


class UserApi(APIView):
    '''
    send info of user over api
    '''

    def get(self, request, format=None):
        users = NewUser.objects.all()
        # important to put many=True
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        permission_classes = [permissions.AllowAny]

        try:
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(
                    {'id': serializer.data.get('userMobile')},
                    status=status.HTTP_201_CREATED,
                )
        except:
            return Response(
                {'Bad Request try again, the user may already exist'},
                status=status.HTTP_404_NOT_FOUND)


class CalculateCost(APIView):
    '''
    calculate the cost of rent of a car given its time duration
    '''

    def post(self, request, format=None):
        print(request.data)
        try:
            to_ = request.data["toDateTime"]
            from_ = request.data["fromDateTime"]
            time_used = int(to_) - int(from_)
            # print(to_, from_)
            post = Car.objects.get(
                carLicenseNumber=request.data["carLicenseNumber"])
            return Response(
                {'Price per Hour': post.pph, 'Total price': post.pph*time_used},
                status=status.HTTP_200_OK)

        except:
            return Response(
                {'Bad Request try again, the number plate may be wrong'},
                status=status.HTTP_404_NOT_FOUND)
