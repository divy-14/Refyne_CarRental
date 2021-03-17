from django.urls import path, include
from . import views

# TODO: add url to figure out which cars are available for a given duration
urlpatterns = [
    path('user/', views.UserApi.as_view(), name="add-user"),
    path('cars/', views.CarApi.as_view(), name="add-car"),
    path('calculate-price/', views.CalculateCost.as_view(), name="price"),
    path('car/book/', views.BookCar.as_view(), name="book-car"),
    path('car/bookings/<pk>', views.Bookers.as_view(), name="car-bookers"),
    path('user/bookings/<int:pk>',
         views.UserBookedCars.as_view(), name="user-booked-cars"),
    path('search-cars/', views.CarsAvailable.as_view(), name="car-bookers"),
]
