from flask_wtf import FlaskForm
from wtforms import StringField


# ImmutableMultiDict([
# ('Field17', u''),
# ('Field14', u'Other site'),
# ('Field12', u'My interests'),
# ('HandshakeKey', u''),
# ('Field11', u'Myself'),
# ('Field27', u'Dafydd referral'),
# ('Field17-url', u''),
# ('Field3', u'Dafydd name'),
# ('DateCreated', u'2017-01-14 05:04:00'),
# ('Field5', u'dafydd@afterpandora.com'),
# ('Field6', u'DuffX'),
# ('EntryId', u'924'),
# ('IP', u'86.155.134.187'),
# ('CreatedBy', u'public'),
# ('Field8', u'Fetlife')])


FIELD_MAPPINGS = {
    'name': 'Field3'
}


class ApplicationForm(FlaskForm):
    # name = StringField('Field3', validators=[DataRequired()])
    Field3 = StringField('Field3')
