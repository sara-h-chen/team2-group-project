SHELL:= /bin/bash

getPythonPackages:
	sudo apt-get install python-pip
	sudo apt-get install python-virtualenv

setVirtualEnv:
	virtualenv env
	source env/bin/activate

installGeospatial:
	sudo apt-get install binutils libproj-dev gdal-bin
	wget http://www.gaia-gis.it/gaia-sins/freexl-sources/freexl-1.0.2.tar.gz
	tar xzf freexl-1.0.2.tar.gz
	cd freexl-1.0.2.tar.gz
	./configure
	make
	sudo make install
	sudo apt-get install libxml2-dev
	wget http://www.gaia-gis.it/gaia-sins/libspatialite-sources/libspatialite-4.3.0.tar.gz
	tar xaf libspatialite-4.3.0.tar.gz
	cd libspatialite-4.3.0
	./configure
	make
	sudo make install

npminstall:
	cd website/backend/geodjango
	npm install --save-dev react webpack webpack-bundle-tracker babel babel-loader
	npm install --save-dev webpack-dev-server react-hot-loader

djangointegration:
	pip install django-webpack-loader

buildwebpack:
	./node_modules/.bin/webpack --config webpack.config.js

