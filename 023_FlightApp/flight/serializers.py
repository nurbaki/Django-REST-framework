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

