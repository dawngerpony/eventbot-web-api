SHELL := /bin/bash

run:
	mongod --dbpath ./data/db

test:
	export `heroku config -s`
	nose2 --verbose
