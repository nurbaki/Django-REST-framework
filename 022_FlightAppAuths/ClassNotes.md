# FlightApp Authentication

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

POSTRESQL_DATABASE = db_name
POSTRESQL_USER = username
POSTRESQL_PASSWORD = password 
POSTRESQL_HOST = localhost
POSTRESQL_PORT = 5432

```

## dj-rest-auth

* https://www.django-rest-framework.org/api-guide/authentication/#django-rest-auth-dj-rest-auth
*  https://dj-rest-auth.readthedocs.io/en/latest/installation.html


```sh

$ pip install dj-rest-auth
# $ pip freeze > requirements.txt

```

create "users" app:

```sh

$ django-admin startapp users

```

main/settings/base.py ->

```py

INSTALLED_APPS = [
    # ...
    'rest_framework',
    'rest_framework.authtoken',
    # ...
    'dj_rest_auth',
    'users',
]

```

main/urls.py ->

```py

urlpatterns = [
    # ...
    path('users/', include('users.urls')),
]

```

users/urls.py:

```py

from django.urls import path, include

urlpatterns = [
    path('auth/', include('dj_rest_auth.urls')),
]

```

```sh

# $ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py runserver

```

* http://127.0.0.1:8000/users/auth/login/
* http://127.0.0.1:8000/users/auth/logout/

## Registration

create users/serializers.py:

```py

from rest_framework import serializers, validators
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import User

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

```

users/views.py:

```py

from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from django.contrib.auth.models import User

from .serializers import RegisterSerializer
from users import serializers

class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    # for special return after serializer.save():
    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # return Response:
        from rest_framework.response import Response
        return Response(
            {
                "message": "User created.",
                "username": request.data.get("username"),
                "email": request.data.get("email"),
                "first_name": request.data.get("first_name"),
                "last_name": request.data.get("last_name"),
            }
        )

```

users/urls.py -> 

```py

from .views import RegisterView

urlpatterns = [
    # ...
    path('register/', RegisterView.as_view()),
]

```

* http://127.0.0.1:8000/users/register/

### TokenSerializer
return user infos with token, after login:

users/serializers.py ->

```py

from dj_rest_auth.serializers import TokenSerializer

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

```

main/settings/base.py ->

```py

REST_AUTH_SERIALIZERS = {
    'TOKEN_SERIALIZER': 'users.serializers.WideTokenSerializer',
}

REST_FRAMEWORK = {
    # Allow post-request without CSRF, so can connection with Token from external service, like Postman:
    'DEFAULT_AUTHENTICATION_CLASSES': ['rest_framework.authentication.TokenAuthentication']
}

```

Download "Postman" for api-testing: https://www.postman.com/downloads/

### Extra:

Download "PostreSQL" Database: https://www.enterprisedb.com/downloads/postgres-postgresql-downloads

    Installation Notes:
    ! For run installation o Windows OS: Right click and "Open with Administrator".
    ! "Stack Builder" will not be selected.
    ! Do not forget setted password. (it is for postgres (admin) user.)

open pgAdmin ->

    Right Click on "Login/Group Roles" and go to Create/Login:
        General -> Name: test
        Definition -> Password: test
        Priviligies -> Can Login: True / Superuser: True
    Righ Click on  "Databases" and go to Create/Database:
        General -> Database: test / Owner: test

.env file:

```sh

SECRET_KEY = you-can-write-random-chars-for-django-secure-code

ENV_NAME = prod

POSTRESQL_DATABASE = test
POSTRESQL_USER = test
POSTRESQL_PASSWORD = test 
POSTRESQL_HOST = localhost
POSTRESQL_PORT = 5432

```

main/settings/prod.py ->

```py

# $ pip install psycopg2 # pip install psycopg2-binary
DATABASES = { 
    "default": { 
        "ENGINE": "django.db.backends.postgresql_psycopg2", 
        "NAME": config("POSTRESQL_DATABASE"), 
        "USER": config("POSTRESQL_USER"), 
        "PASSWORD": config("POSTRESQL_PASSWORD"), 
        "HOST": config("POSTRESQL_HOST"), 
        "PORT": config("POSTRESQL_PORT"), 
        "ATOMIC_REQUESTS": True, 
    }
} 

```

```sh

$ python manage.py migrate
$ python manage.py createsuperuser
$ python manage.py runserver

```