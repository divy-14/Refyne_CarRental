from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from .serializers import CarSerializer, UserSerializer, BookCarSerializer
from .models import Car, NewUser, BookedCars
from rest_framework import status, permissions
from rest_framework.response import Response
from datetime import datetime
from dateutil import parser
from rest_framework.renderers import JSONRenderer


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


class BookCar(APIView):
    '''
    Book a car for a given duration
    '''

    def post(self, request, format=None):
        booked_cars = BookedCars.objects.all()
        cars = Car.objects.all()
        users = NewUser.objects.all()
        mobileNum = request.data['userid']
        to_ = request.data["toDate"]
        from_ = request.data["fromDate"]
        carNumber = request.data["carLicenseNumber"]

        to_ = datetime.strptime(to_, '%Y-%m-%d %H:%M:%S')
        from_ = datetime.strptime(from_, '%Y-%m-%d %H:%M:%S')

        if to_ < from_:
            return Response(
                {'Not possible end date has to be greater than start date'},
                status=status.HTTP_403_FORBIDDEN)

        # user not found in the user database
        FoundUser = False
        for user in users:
            if int(user.userMobile) == int(mobileNum):
                FoundUser = True

        if FoundUser == False:
            return Response(
                {'User with given mobile number/id not Found'},
                status=status.HTTP_404_NOT_FOUND)

        # car with the given numberplate not in the car database
        FoundPlate = False
        for obj in cars:
            # comparing strings imp..
            if str(obj.carLicenseNumber) == str(carNumber):
                FoundPlate = True

        if FoundPlate == False:
            return Response(
                {'Car with given number plate not Found'},
                status=status.HTTP_404_NOT_FOUND)

        # different conditions
        else:
            time_intervals = []
            availableAfter = None  # we will find what is the time after which a car is available
            for obj in booked_cars:
                if str(obj.carLicenseNumber) == str(carNumber):
                    time_intervals.append(
                        (obj.fromDate.replace(tzinfo=None), obj.toDate.replace(tzinfo=None)))
                    if availableAfter is None:
                        availableAfter = obj.toDate
                    else:
                        availableAfter = max(availableAfter, obj.toDate)

            time_intervals.sort()

            # if the car is not yet booked by anyone
            if availableAfter == None:
                serializer = BookCarSerializer(data=request.data)
                permission_classes = [permissions.AllowAny]

                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    return Response(serializer.data)

            # if the car in not available in the given interval
            for time in time_intervals:
                if from_ < time[1] and from_ >= time[0]:
                    return Response(
                        {'Car not available:': carNumber,
                         'Car Booked for:': time},
                        status=status.HTTP_403_FORBIDDEN)

                if from_ <= time[0] and to_ >= time[1]:
                    return Response(
                        {'Car not available:': carNumber,
                         'Car Booked for:': time},
                        status=status.HTTP_403_FORBIDDEN)

                if to_ > time[0] and to_ <= time[1]:
                    return Response(
                        {'Car not available:': carNumber,
                         'Car Booked for:': time},
                        status=status.HTTP_403_FORBIDDEN)

            # else if the car is available we book it
            serializer = BookCarSerializer(data=request.data)
            permission_classes = [permissions.AllowAny]

            try:
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    return Response(serializer.data)
            except:
                return Response(status=status.HTTP_404_NOT_FOUND)


class Bookers(APIView):

    def get(self, request, pk=None, format=None):
        carId = str(pk)
        booked_cars = BookedCars.objects.filter(carLicenseNumber=carId)
        serializer = BookCarSerializer(booked_cars, many=True)

        json_data = JSONRenderer().render(serializer.data)
        return HttpResponse(json_data, content_type="application/json")


class UserBookedCars(APIView):
    def get(self, request, pk=None, format=None):
        userId = pk
        booked_cars = BookedCars.objects.filter(userid=userId)
        serializer = BookCarSerializer(booked_cars, many=True)

        json_data = JSONRenderer().render(serializer.data)
        return HttpResponse(json_data, content_type="application/json")


'''
3 cases:
car booked for [(27, 29)], car booking request for examples:
1. [(27, 29)]  -> incoming (24, 30) return False
2. [(27, 29)]  -> incoming (24, 28) return False
3. [(27, 29)]  -> incoming (28, 31) return False
4. [(24, 30)]  -> incoming (27, 29) return False
'''
