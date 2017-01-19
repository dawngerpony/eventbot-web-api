#!/usr/bin/env bash
# https://docs.mongodb.com/manual/reference/program/mongoimport/
FILENAME="members_export_3f3e9231f0.csv"
mongoimport --db mailchimp --type csv --headerline --verbose ${FILENAME}
