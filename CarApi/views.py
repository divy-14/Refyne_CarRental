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
from collections import defaultdict
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class CarApi(APIView):

    def get(self, request, format=None):
        '''
        get info of all the cars in the database
        '''
        cars = Car.objects.all()
        # important to put many=True
        serializer = CarSerializer(cars, many=True)
        return Response(serializer.data)

    schema = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'carLicenseNumber': openapi.Schema(type=openapi.TYPE_STRING, description='The license Plate number for the car'),
            'Manufacturer': openapi.Schema(type=openapi.TYPE_STRING, description='The Manufacturer of the Car'),
            'Model': openapi.Schema(type=openapi.TYPE_STRING, description='The city to which the car belongs to'),
            'base_price': openapi.Schema(type=openapi.TYPE_INTEGER, description='The base price of the Car'),
            'pph': openapi.Schema(type=openapi.TYPE_INTEGER, description='The price per hour of the Car for rental'),
            'security_deposit': openapi.Schema(type=openapi.TYPE_INTEGER, description='The security deposit for the Car'),
        })

    @swagger_auto_schema(request_body=schema)
    def post(self, request, format=None):
        '''
        post details about a new car
        '''
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
            return Response(status=status.HTTP_404_NOT_FOUND)


class UserApi(APIView):

    def get(self, request, format=None):
        '''
        get info about a particular user
        '''
        users = NewUser.objects.all()
        # important to put many=True
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    schema = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'userName': openapi.Schema(type=openapi.TYPE_STRING, description='The name of the user'),
            'userMobile': openapi.Schema(type=openapi.TYPE_INTEGER, description='The phone number of the user'),
        })

    @swagger_auto_schema(request_body=schema)
    def post(self, request, format=None):
        '''
        post info about a new user
        '''
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
            return Response(status=status.HTTP_404_NOT_FOUND)


class CalculateCost(APIView):
    '''
    calculate the cost of rent of a car given its time duration
    '''
    schema = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'carLicenseNumber': openapi.Schema(type=openapi.TYPE_STRING, description='The license number for the car'),
            'fromDate': openapi.Schema(type=openapi.TYPE_STRING, description='Start Jouney Date and Time, format-> %Y-%m-%d %H:%M:%S'),
            'toDate': openapi.Schema(type=openapi.TYPE_STRING, description='End Date for your Journey, format-> %Y-%m-%d %H:%M:%S'),
        })

    @swagger_auto_schema(request_body=schema)
    def post(self, request, format=None):
        try:
            to_ = request.data["toDate"]
            from_ = request.data["fromDate"]
            to_ = datetime.strptime(to_, '%Y-%m-%d %H:%M:%S')
            from_ = datetime.strptime(from_, '%Y-%m-%d %H:%M:%S')

            if to_ < from_:
                return Response(
                    {'Not possible end date has to be greater than start date'},
                    status=status.HTTP_403_FORBIDDEN)

            # time used is in seconds
            time_used = to_ - from_

            car = Car.objects.get(
                carLicenseNumber=request.data["carLicenseNumber"])
            hours_used = time_used//3600
            ans = car.pph*hours_used
            return Response(
                {
                    'Price per Hour': car.pph,
                    'Total Hours': hours_used,
                    'Total price': ans
                },
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

    '''
    get list of users who have booked a given car
    '''

    def get(self, request, pk=None, format=None):
        carId = str(pk)
        try:
            booked_cars = BookedCars.objects.filter(carLicenseNumber=carId)
            if not booked_cars:
                return Response(status=status.HTTP_404_NOT_FOUND)

            serializer = BookCarSerializer(booked_cars, many=True)
            json_data = JSONRenderer().render(serializer.data)
            return HttpResponse(json_data, content_type="application/json")
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)


class UserBookedCars(APIView):
    '''
    return a list of cars booked by the user
    '''

    def get(self, request, pk=None, format=None):
        userId = pk
        booked_cars = BookedCars.objects.filter(userid=userId)
        users = NewUser.objects.filter(userMobile=userId)

        if len(users) == 0:
            return Response(
                {'User not Found': userId},
                status=status.HTTP_404_NOT_FOUND)

        serializer = BookCarSerializer(booked_cars, many=True)

        json_data = JSONRenderer().render(serializer.data)
        return HttpResponse(json_data, content_type="application/json")


class CarsAvailable(APIView):
    '''
    searches for car in a given time interval
    '''

    schema = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'fromDate': openapi.Schema(type=openapi.TYPE_STRING, description='Start Jouney Date and Time, format-> %Y-%m-%d %H:%M:%S'),
            'toDate': openapi.Schema(type=openapi.TYPE_STRING, description='End Date for your Journey, format-> %Y-%m-%d %H:%M:%S'),
        })

    @swagger_auto_schema(request_body=schema)
    def post(self, request, format=None):
        to_ = request.data["toDate"]
        from_ = request.data["fromDate"]

        # converting to and from to datetime objects
        to_ = datetime.strptime(to_, '%Y-%m-%d %H:%M:%S')
        from_ = datetime.strptime(from_, '%Y-%m-%d %H:%M:%S')

        # if from_ is greater than to_ date return as this is not possible
        if to_ < from_:
            return Response(
                {'Not possible end date has to be greater than start date'},
                status=status.HTTP_403_FORBIDDEN)

        # getting list of booked car and all the cars available
        booked_cars = BookedCars.objects.all()
        cars = Car.objects.all()

        # we will use a dictionary to keep track of all the cars
        cars_schedule = {}

        # adding all the cars in our arsenal to the car_schedule list
        for car in cars:
            if str(car.carLicenseNumber) not in cars_schedule:
                cars_schedule[car.carLicenseNumber] = []

        # now each car will have a list of its booking schedule
        for car in booked_cars:
            fromDate = car.fromDate.replace(tzinfo=None)
            toDate = car.toDate.replace(tzinfo=None)
            cars_schedule[str(car.carLicenseNumber)].append((fromDate, toDate))

        # this list will keep track of available cars
        available_cars = []

        for car in cars_schedule:

            # Now if a car has no booking its car_schedule list will be
            # empty and any user can book it
            if len(cars_schedule[car]) == 0:
                available_cars.append(car)
                continue

            # else we take a note of each cars schedule sort it
            # and then check if the car is available for the reqd duration
            cars_schedule[car].sort
            is_available = True  # we assume car is available
            for time in cars_schedule[car]:
                if from_ < time[1] and from_ >= time[0]:
                    is_available = False
                    break
                if from_ <= time[0] and to_ >= time[1]:
                    is_available = False
                    break
                if to_ > time[0] and to_ <= time[1]:
                    is_available = False
                    break
            if is_available == True:
                available_cars.append(car)

        return Response(
            {'Cars Avaiable for given duration': available_cars}
        )


'''
3 cases:
car booked for [(27, 29)], car booking request for examples:
1. [(27, 29)]  -> incoming (24, 30) return False
2. [(27, 29)]  -> incoming (24, 28) return False
3. [(27, 29)]  -> incoming (28, 31) return False
4. [(24, 30)]  -> incoming (27, 29) return False
'''
