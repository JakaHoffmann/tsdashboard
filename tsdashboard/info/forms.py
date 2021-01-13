from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, BooleanField, SelectField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, URL
from wtforms.fields.html5 import DateField


class InfoForm(FlaskForm): # pass
    zanimivi_primeri = TextAreaField('zanimivi primeri', render_kw={"placeholder": "zanimiv primer ...", "onkeyup": "textareaAutoHeight(this)", "onclick": "ustvariDatum(this.id)"})
    zanimivi_primeri_cas = DateField('zanimivi_primeri_cas', format='%Y-%m-%d')
    opazanja = TextAreaField('opažanja', render_kw={"placeholder": "opazil sem ...", "onkeyup": "textareaAutoHeight(this)", "onclick": "ustvariDatum(this.id)"})
    opazanja_cas = DateField('opazanja_cas', format='%Y-%m-%d')
    dolgotrajne_napake = TextAreaField('dolgotrajne napake', render_kw={"placeholder": "tale inc se vleče že ...", "onkeyup": "textareaAutoHeight(this)", "onclick": "ustvariDatum(this.id)"})
    dolgotrajne_napake_cas = DateField('dolgotrajne_napake_cas', format='%Y-%m-%d')
    projekti = TextAreaField('projekti', render_kw={"placeholder": "sodeloval sem pri ...", "onkeyup": "textareaAutoHeight(this)", "onclick": "ustvariDatum(this.id)"})
    projekti_cas = DateField('projekti_cas', format='%Y-%m-%d')
    ostalo = TextAreaField('ostalo', render_kw={"placeholder": "mogoče lahko izboljšamo ...", "onkeyup": "textareaAutoHeight(this)", "onclick": "ustvariDatum(this.id)"})
    ostalo_cas = DateField('ostalo_cas', format='%Y-%m-%d')

    submit = SubmitField('dodaj info')