SHELL := /bin/bash

local:
	heroku local web

run:
	mongod --dbpath ./data/db

test:
	export `heroku config -s`
	nose2 --verbose
