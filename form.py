from wtforms import Form, StringField, FileField, SelectField, TextAreaField, PasswordField, validators

# ------------- Form classes that connects to the database ------------- #


# Class for missing dog form
class AddDogForm(Form):
    dogName = StringField('The dogs name', [validators.Length(min=1, max=200)])
    dogAge = StringField('The dogs age', [validators.Length(min=1, max=200)])
    owner = StringField('Name of the owner',
                        [validators.Length(min=1, max=200)])
    home = StringField('Streetname of the dogs home',
                       [validators.Length(min=1, max=200)])
    lastSeen = StringField('Place it was last seen',
                           [validators.Length(min=1, max=200)])
    comments = StringField('Any additional comments?',
                           [validators.Length(min=0, max=1000)])
    area = SelectField(u'area',
                       choices=[('101 Reykjavík', '101 Reykjavík'),
                                ('102 Reykjavík', '102 Reykjavík'),
                                ('103 Reykjavík', '103 Reykjavík'),
                                ('104 Reykjavík', '104 Reykjavík'),
                                ('105 Reykjavík', '105 Reykjavík'),
                                ('107 Reykjavík', '107 Reykjavík'),
                                ('108 Reykjavík', '108 Reykjavík'),
                                ('109 Reykjavík', '109 Reykjavík'),
                                ('110 Reykjavík', '110 Reykjavík'),
                                ('111 Reykjavík', '111 Reykjavík'),
                                ('112 Reykjavík', '112 Reykjavík'),
                                ('113 Reykjavík', '113 Reykjavík'),
                                ('116 Reykjavík', '116 Reykjavík'),
                                ('170 Seltjarnarnes', '170 Seltjarnarnes'),
                                ('200 Kópavogur', '200 Kópavogur'),
                                ('201 Kópavogur', '201 Kópavogur'),
                                ('203 Kópavogur', '203 Kópavogur'),
                                ('206 Kópavogur', '206 Kópavogur'),
                                ('210 Garðabær ', '210 Garðabær'),
                                ('220 Hafnarfjörður', '220 Hafnarfjörður'),
                                ('221 Hafnarfjörður', '221 Hafnarfjörður')])
    img = StringField('add image', [validators.Length(min=0, max=10000)])


class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')
