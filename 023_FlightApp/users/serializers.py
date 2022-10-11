from rest_framework import serializers
from django.contrib.auth.models import User

from rest_framework import validators # for email
from django.contrib.auth.password_validation import validate_password # for password

class RegisterSerializer(serializers.ModelSerializer):
    # Customization:
    email = serializers.EmailField(
        required = True,
        validators = [validators.UniqueValidator(queryset=User.objects.all())],
    )
    password = serializers.CharField(
        required = True,
        write_only = True,
        style = {"input_type": "password"},
        # validators = [validate_password], # Use rules from settings.
    )
    password2 = serializers.CharField(
        required = True,
        write_only = True,
        style = {"input_type": "password"},
        # validators = [validate_password], # Use rules from settings.
    )

    # change default settings:
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

    # check validates:
    def validate(self, attrs):
        # if error:
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"message": "Passwords are not same."}
            )
        # else:
        return attrs
    
    # create new user:
    def create(self, validated_data):
        # remove password from dict():
        validated_data.pop("password2") 
        # create new user:
        user = User.objects.create(**validated_data)
        # encrypt password:
        password = validated_data.get("password")
        user.set_password(password)
        # update:
        user.save()
        return user

# ---------------------------------------------
# TOKEN Override:

from dj_rest_auth.serializers import TokenSerializer

'''
# Aşağıdaki Serializer user verisi içindir. Aynı datayı RegisterSerializer'dan çektik.
class UserTokenSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
        )
'''

class WideTokenSerializer(TokenSerializer):

    # user = UserTokenSerializer(read_only=True)
    user = RegisterSerializer(read_only=True)
    
    class Meta(TokenSerializer.Meta):
        fields = (
            'key',
            'user'
        )