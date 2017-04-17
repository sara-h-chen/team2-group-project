# team2-group-project

## Group Project

### Backend

#### Installation

Most of the backend runs on Python 2.7, which was chosen due to the fact that it is available by default on both Linux and MacOS.

With Python installed, the server can now run on the Django framework and its extension, Django Rest Framework. Both of this can be installed through `pip`, Python's package manager, on the command line by typing the following command:
`pip install django djangorestframework`

These packages are installed into a virtual environment, which maintains the same Python configurations throughout the project. The virtual environment is stored within the django/ folder and can be entered by typing the following command:
`source django/bin/activate`

This folder containing the virtual environment is uploaded to the server, where it is activated, and as such, the app does not require further installation on the server.

### Frontend

The static files for the website are hosted on the server, and is then served directly to the client upon request. As the frontend runs solely on JavaScript and jQuery, which is supported by most modern web browsers by default, no installation is required.
