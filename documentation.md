# Team 2 Group Project Documentation

### Frontend

The static files of the frontend is hosted entirely on community.dur.ac.uk, which then makes calls to the backend hosted on PythonAnywhere, an external service.

The frontend runs solely on jQuery and JavaScript. The responsive layout is built on top of Bootstrap, which is imported into the HTML files along with jQuery in the header of the HTML file, using a CDN. Based on modern web architecture, which aims to reduce the load on the server, light processing is carried out on the client side, such as sorting.

AJAX calls are then made to the server, with JSON being the medium of choice.

#### Authentication

The `auth-token` provided by the backend upon successful authentication is stored as a cookie in the frontend, and is used to identify the user of the current session. The value of the cookie is sent along with the request to the backend, which is then able to authorize and identify the user.

### Backend

This project is implemented with Django, Django REST framework, and SQLite on PythonAnywhere.com.

The backend is implemented in both Django and the Django REST framework, with Django templating used in tandem with Django's in built User models, which allows for a quick password reset mechanism to be set up. The structure of the database is defined in `models.py`, and is created as Python classes. Django converts this into a SQLite structure automatically, through the following command, which refreshes the current database structure:

`python manage.py makemigrations`

Once the changes are confirmed, the following command would cause Django to rebuild the database:

`python manage.py migrate`

To begin running the development server for testing purposes, the following command is used:

`python manage.py runserver`


#### Database Structures
The `serializers.py` class contains the serializers that convert Python objects into a Model and vice versa, allowing them to be processed, e.g. encoded into a JSON object. Classes made in the `models.py` script are given serializers which specify the fields that will be included when the object is serialized into a JSON object. The use of slug-related fields allows the power of foreign keys to be exploited without directly having to manipulate database queries.

The `urls.py` script defines which views (refer below) are displayed at the URL endpoint.

The `views.py` script defines the functions that are called when an endpoint is accessed. Each of them are decorated with `@API_View`, which means that the request at the endpoint is first passed through Django REST Framework's middleware. This allows the framework to extract metadata from the request, including the identity of the current user, and for the authentication process to be carried out, using the token provided by the frontend. The decorator functions also allow for permissions to be placed upon an object, and as such, prohibits a user from making changes to an object that does not belong to the user. The contents of the requests are then converted into Python objects, using the serializer.

When user accounts are created, passwords are hashed before being stored in the database, and are not stored in plaintext. This gives the database a layer of security. Password verifiers were also installed by default with Django, ensuring that passwords given by users meet a certain standard before users are allowed to create an account. 

All images uploaded to the server are handled as base-64 strings, which increase the size of the image by 33%, but make transfers between the backend and frontend simpler. This is not a scalable solution, however, and would need to be replaced with binary storage when scalability becomes necessary.
