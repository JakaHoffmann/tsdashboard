from flask import Blueprint, render_template, redirect, flash
from flask_login import current_user, login_required

from tsdashboard.info.forms import InfoForm


info = Blueprint('info', __name__)

@info.route('/info')
@login_required
def informacije(): # pass
    form = InfoForm()
    if form.validate_on_submit():
        info = InfoModel(
            zanimivi_primeri=form.zanimivi_primeri.data,
            zanimivi_primeri_cas=form.zanimivi_primeri_cas.data,
            opazanja=form.opazanja.data,
            opazanja_cas=form.opazanja_cas.data,
            dolgotrajne_napake=form.dolgotrajne_napake.data,
            dolgotrajne_napake_cas=form.dolgotrajne_napake_cas.data,
            projekti=form.projekti.data,
            projekti_cas=form.projekti_cas.data,
            ostalo=form.ostalo.data,
            ostalo_cas=form.ostalo_cas.data)


        db.session.add(info)
        db.session.commit()
        flash(f'uspešno dodan SIEM API', 'success')
        return redirect(url_for('APIs'))
    return render_template('info.html', title='Informacije', name='Info', form=form)

@info.route('/info/<datum>')
@login_required
def dogodek(datum):
    return render_template('dogodek.html', title='Dogodki', name=datum, data=datum)