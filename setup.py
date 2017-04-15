from distutils.core import setup

setup(
    name='eventbot-web-api',
    version='0.1.0',
    packages=[
        'eventbot',
        'eventbot.app',
        'eventbot.app.eventbrite',
        'eventbot.app.mailchimp',
        'eventbot.app.slack',
    ],
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    long_description=open('README.md').read(),
)
