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
