from django.urls import path, include
from . import views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Refyne CarRental API",
        default_version='v1',
        description="An API for managing CAR Rentals",
        contact=openapi.Contact(email="divymohanrai@gmail.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# TODO: add url to figure out which cars are available for a given duration
urlpatterns = [
    path('', schema_view.with_ui('swagger',
                                 cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc',
                                       cache_timeout=0), name='schema-redoc'),
    path('user/', views.UserApi.as_view(), name="add-user"),
    path('cars/', views.CarApi.as_view(), name="add-car"),
    path('calculate-price/', views.CalculateCost.as_view(), name="price"),
    path('car/book/', views.BookCar.as_view(), name="book-car"),
    path('car/bookings/<pk>', views.Bookers.as_view(), name="car-bookers"),
    path('user/bookings/<int:pk>',
         views.UserBookedCars.as_view(), name="user-booked-cars"),
    path('search-cars/', views.CarsAvailable.as_view(), name="car-bookers"),
]
