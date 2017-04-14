#!make
# http://unix.stackexchange.com/questions/235223/makefile-include-env-file
# include .env
# export $(shell sed 's/=.*//' .env)


SHELL := /bin/bash

local:
	heroku local dev

db:
	mongod --dbpath ./data/db

test:
	heroku local test
