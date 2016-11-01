# Team 2 Group Project Documentation

## Frontend

## Backend

This project is implemented with Django, Django REST framework, and SQLite3.

The backend is being run by the Django REST framework, which provides us with an API to access the database (Alternatively, you can access the database manually using SQLite3). The structure of the database is defined in ~~~ website/backend/geodjango/location/models.py ~~~, and is created as Python classes. Django converts this into an SQLite structure automatically. After making any changes to the structure of the database, Django needs to refresh the structure that it currently has, so:

~~~ python manage.py makemigrations ~~~

shows you the changes made to the structure of the database. Once you have confirmed the changes, typing the following command would cause Django to rebuild the database:

~~~ python manage.py migrate ~~~

To begin running the development server, type in the following command:

~~~ python manage.py runserver ~~~


### Database Structures
The ~~~ serializers.py ~~~ class in ~~~ website/backend/geodjango/location ~~~ contains the serializers which converts the Python object into a Model, which allows it to be processed. Any classes that have been made in the ~~~ models.py ~~~ script must have its own serializer, otherwise, Django will not be able to display it on its API.

The ~~~ urls.py ~~~ script allows you to define which pages you would like to have displayed when accessing the defined URLs.

~~~ views.py ~~~ allows you to define what information you would like displayed on the URL defined above.
