# from django.urls import path
# 
# urlpatterns = [
#   path('', function_name)
# ]

from rest_framework import routers
from .views import (
    FlightView,
    PassengerView,
    ReservationView,
)

# after "/flight/":
router = routers.DefaultRouter()
router.register('flights', FlightView)
router.register('passengers', PassengerView)
router.register('reservations', ReservationView)
urlpatterns = router.urls