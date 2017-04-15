dev: gunicorn eventbot.run:app --log-file=- --reload
web: gunicorn eventbot.run:app --log-file=-

test: nose2 --verbose

testlog: nose2 --verbose --log-capture
