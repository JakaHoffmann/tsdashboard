from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, BooleanField, SelectField, IntegerField
from wtforms.validators import DataRequired, URL
from wtforms.fields.html5 import DateField


class ApiForm(FlaskForm):
    ime_uporabnika = StringField('Ime uporabnika', validators=[DataRequired()])
    izbor_SIEM = SelectField('Izbor SIEMa', validators=[DataRequired()], choices=[('', 'izberi SIEM'), ('qradar', 'QRadar'), ('mcafee', 'McAfee'), ('splunk', 'Splunk')])
    api_kluc = StringField('API key', validators=[DataRequired()])
    url = StringField('URL', validators=[DataRequired(), URL()])
    api_admin_dostop = BooleanField('API admin dostop')
    izdelava_statistike = BooleanField('Izdelava statistike')

    cas_preverbe = IntegerField('na koliko časa preverim stanje', validators=[DataRequired()])
    cas_opozorila = IntegerField('po kolikšnem časa opozorimo za neprevzete offense', validators=[DataRequired()])

    submit = SubmitField('Dodaj API')
    submit1 = SubmitField('Popravi API')