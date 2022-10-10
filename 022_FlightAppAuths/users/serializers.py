from rest_framework import serializers, validators
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import User
from dj_rest_auth.serializers import TokenSerializer

class RegisterSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(
        required = True,
        validators = [validators.UniqueValidator(queryset=User.objects.all())]
        #! unique = True, # This method not support on Serializers.
    )

    password = serializers.CharField(
        required = True,
        write_only = True,
        validators = [validate_password], # for passsword rules (visit settings)
        style = {"input_type": "password"} # for API Template
    )

    password2 = serializers.CharField(
        required = True,
        write_only = True,
        validators = [validate_password], # for passsword rules (visit settings)
        style = {"input_type": "password"} # for API Template
    )

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'password',
            'password2',
        )
    
    def create(self, validated_data):
        password = validated_data.get("password") # alternate using -> validated_date["password"]
        validated_data.pop("password2") # Must not be in saving records.
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def validate(self, data):
        if data["password"] != data["password2"]:
            raise serializers.ValidationError({"message": "Passwords are not same."})
        return data


class UserTokenSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
        )

class WideTokenSerializer(TokenSerializer):

    user = UserTokenSerializer(read_only=True)

    class Meta(TokenSerializer.Meta):
        fields = ('key', 'user')