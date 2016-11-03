# team2-group-project

## Group Project


### Backend

#### Installations

Before running the server, a few things need to be installed. Go into the project's root folder directory, and you should see a Makefile. I've included most of the commands needed for you to install the package dependencies that you need to run the server, so you just need to type:

`make getPythonPackages`

This installs pip (if you don't already have it installed), and the virtualenv tool. The virtual environment ensures that any installations you make are not carried across your system, and are isolated to just this project. You can enter the virtual environment by typing:

`make setVirtualEnv`

The following packages are required to run the Django REST framework, and they can both be downloaded with:

`make djangointegration`

