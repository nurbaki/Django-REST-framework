from django.shortcuts import render
from rest_framework import viewsets

from .models import (
    Flight,
    Passenger,
    Reservation,
)
from .serializers import (
    FlightSerializer,
    PassengerSerializer,
    ReservationSerializer,
)
from .permissions import (
    IsStaffPermission
)


# /flight/flights/:
class FlightView(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    permission_classes = [IsStaffPermission] # Only StaffUser

    # view all details for staff-user:
    def get_serializer_class(self):
        if self.request.user.is_staff:
            # return new serializer:
            from .serializers import FlightForStaffsSerializer
            return FlightForStaffsSerializer
        else:
            # return default:
            return super().get_serializer_class()


# /flight/passengers/:
class PassengerView(viewsets.ModelViewSet):
    queryset = Passenger.objects.all()
    serializer_class = PassengerSerializer
    # permission_classes = [IsStaffPermission]


# /flight/reservations/:
class ReservationView(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    # permission_classes = [IsStaffPermission]

    # view limited records:
    def get_queryset(self):
        # queryset = Reservation.objects.all()
        # queryset = super().get_queryset()
        queryset = self.queryset

        if self.request.user.is_staff:
        # user is staff: view all:
            return queryset
        else:
        # user is not staff: view only own-records:
            return queryset.filter(user=self.request.user)

