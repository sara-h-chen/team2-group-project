SHELL:= /bin/bash

getPythonPackages:
	sudo apt-get install python-pip
	sudo apt-get install python-virtualenv
	sudo apt-get install python-mysqldb
	sudo apt-get install libmysqlclient-dev

setVirtualEnv:
	virtualenv env
	source env/bin/activate

djangointegration:
	pip install coreapi

