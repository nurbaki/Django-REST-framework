# FlightApp API

```sh

$ python -m venv env
$ source env/bin/activate
$ pip install -r requirements.txt
# $ mv sample.env .env # rename
$ python manage.py migrate
$ python manage.py createsuperuser
# $ python manage.py runserver

```

.env file:

```sh

SECRET_KEY = you-can-write-random-chars-for-django-secure-code

ENV_NAME = dev

POSTRESQL_DATABASE = dbname
POSTRESQL_USER = username
POSTRESQL_PASSWORD = password 
POSTRESQL_HOST = localhost
POSTRESQL_PORT = 5432

```

create "flight" app:

```sh

$ django-admin startapp flight

```

main/settings/base.py ->

```py

INSTALLED_APPS = [
    # ...
    'flight',
]

```

flight/models.py:

```py

from django.db import models

class FixModel(models.Model):
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True # for "NOT CREATE" table on run migrate.

class Flight(FixModel):
    flight_number = models.CharField(max_length=10) # Uçuş No
    operation_airlines = models.CharField(max_length=15) # Havayolu Şirketi
    departure_city = models.CharField(max_length=30) # Kalkış: Nereden
    arrival_city = models.CharField(max_length=30) # Varış: Nereye
    date_of_departure = models.DateField() # Kalkış: Tarih
    time_of_departure = models.TimeField() # Kalkış: Tahmini Saat
    #! from FixModel:
    # created_time = models.DateTimeField(auto_now_add=True)
    # updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'[ {self.flight_number} ] {self.departure_city} -> {self.arrival_city} # {self.date_of_departure} {self.time_of_departure}'

class Passenger(FixModel):
    first_name = models.CharField(max_length=50) # Yolcu Adı
    last_name = models.CharField(max_length=50) # Yolcu Soyadı
    email = models.EmailField(blank=True, null=True) # Yolcu E-Posta
    phone_number = models.IntegerField(blank=True, null=True) # Yolcu Telefon

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


from django.contrib.auth.models import User
#! related_name, It is for reverse-calling. (can use "passenger" instead of "passenger_set")
class Reservation(FixModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE) # Rezervasyon Yapan KULLANICI.
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name="flight_reservations") # Rezervasyon Yapılan UÇUŞ.
    passenger = models.ManyToManyField(Passenger, related_name="passenger_reservations") # Rezervasyon yapılan YOLCULAR.

    def __str__(self):
        return f'Reservation: {self.flight.flight_number} / Passengers: {self.passenger.count()}'

```

flight/admin.py:

```py

from django.contrib import admin

from .models import *
admin.site.register(Flight)
admin.site.register(Passenger)
admin.site.register(Reservation)

```

main/urls.py ->

```py

urlpatterns = [
    # ...
    path('flight/', include('flight.urls')),
]

```

create flight/serializers.py:

```py

from wsgiref import validate
from rest_framework import serializers
from .models import (
    Flight,
    Passenger,
    Reservation,
)

class FlightSerializer(serializers.ModelSerializer):

    class Meta:
        model = Flight
        # fields = '__all__'
        fields = (
            "id",
            # "created_time",
            # "updated_time",
            "flight_number",
            "operation_airlines",
            "departure_city",
            "arrival_city",
            "date_of_departure",
            "time_of_departure",
        )

class PassengerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Passenger
        # fields = '__all__'
        exclude = (
            "created_time",
            "updated_time",
        )

class ReservationSerializer(serializers.ModelSerializer):
    # Nested Serailizers:
    passenger = PassengerSerializer(many=True,  required=False)
    # flight = FlightSerializer(required=False)
    flight = serializers.StringRelatedField()
    user = serializers.StringRelatedField() # default = read_only

    # set relation IDs:
    flight_id = serializers.IntegerField()
    user_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Reservation
        fields = '__all__'

    def create(self, validated_data):
         # Cut passengers from data:
        passenger_data = validated_data.pop('passenger')
         # Add current user_id to data:
        validated_data['user_id'] = self.context['request'].user.id
        # Create:
        reservation = Reservation.objects.create(**validated_data)
        # Create and Add Passengers:
        for passenger in passenger_data:
            new_passenger = Passenger.objects.create(**passenger)
            reservation.passenger.add(new_passenger)
        # Update reservation with passenger_ids:
        reservation.save()
        return reservation

# Special Serializer for Staff Viewing:
class FlightForStaffsSerializer(serializers.ModelSerializer):

    # ! "flight_reservations" name is related_name in models.
    flight_reservations = ReservationSerializer(many=True, read_only=True)

    class Meta:
        model = Flight
        fields = (
            "id",
            "flight_number",
            "operation_airlines",
            "departure_city",
            "arrival_city",
            "date_of_departure",
            "time_of_departure",
            "created_time",
            "updated_time",
            # view reservation details:
            "flight_reservations",
        )


```

flight/views.py:

```py

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

```

create flight/urls.py:

```py

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

```

create flight/permissions.py:

```py

from urllib import request
from rest_framework import permissions

class IsStaffPermission(permissions.IsAdminUser):
    # check permission:
    def has_permission(self, request, view):
        if request.auth:
        # is login:
            if request.method in permissions.SAFE_METHODS:
            # All member can view:
                return True
            else:
            # Only staff-member can run POST/PUT/DELETE:
                return bool(request.user.is_staff)
        # is not login:
        return False

```
