from django.urls import path, include
from . import views

urlpatterns = [
    path('user/', views.UserApi.as_view(), name="add-user"),
    path('cars/', views.CarApi.as_view(), name="add-car"),
    path('calculate-price/', views.CalculateCost.as_view(), name="price")

]
