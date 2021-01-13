from flask import url_for, render_template, redirect, request, flash, Blueprint
from flask_login import current_user, login_required

from tsdashboard import db, scheduler
from tsdashboard.models import ApiModel
from tsdashboard.apis.forms import ApiForm
from tsdashboard.utile import app_scheduler
from tsdashboard.utile.siem import Qradar, QradarConfig

apis = Blueprint('apis', __name__)

@apis.route('/APIs')
@login_required
def APIs():
    apis = ApiModel.query.all()
    return render_template('allAPIs.html', title='APIs', name='APIs', apis=apis)

@apis.route('/APIs/add', methods=['GET', 'POST'])
@login_required
def APIadd():
    form = ApiForm()
    if form.validate_on_submit():
        siem = ApiModel(
            ime=form.ime_uporabnika.data,
            izbor=form.izbor_SIEM.data,
            api_key=form.api_kluc.data,
            url=form.url.data,
            barva=request.form.getlist('apiBarva')[0],
            admin_dostop=form.api_admin_dostop.data,
            statistika=form.izdelava_statistike.data,
            cas_spremljanja=form.cas_preverbe.data,
            cas_opozorila=form.cas_opozorila.data,
            user_id=current_user.username
            )
        
        db.session.add(siem)
        db.session.commit()
        flash(f'uspešno dodan SIEM API', 'success')
        if form.izbor_SIEM.data == "qradar":
            if form.api_admin_dostop.data is True:
                config = QradarConfig(form.ime_uporabnika.data, form.api_kluc.data, form.url.data, form.api_admin_dostop.data)
                config.setDomains()
                config.setOffenses()
                scheduler.add_job(id="{}".format(form.ime_uporabnika.data), func=app_scheduler.updateQradar, trigger="interval", seconds=form.cas_preverbe.data, replace_existing=True)
            else:
                config = QradarConfig(form.ime_uporabnika.data, form.api_kluc.data, form.url.data, form.api_admin_dostop.data)
                config.setOffenses()
                scheduler.add_job(id="{}".format(form.ime_uporabnika.data), func=app_scheduler.updateQradar, trigger="interval", seconds=form.cas_preverbe.data, replace_existing=True)
        elif form.izbor_SIEM.data == "mcafee":
            pass
        elif form.izbor_SIEM.data == "splunk":
            pass
        else:
            print("nic izbranega")
        return redirect(url_for('apis.APIs'))
    return render_template('APIadd.html', title="Dodaj API", name='Dodaj API', form=form)

@apis.route('/APIs/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def APIedit(id):
    #################################################################
    api = ApiModel.query.get_or_404(id)
    form = ApiForm()
    if form.validate_on_submit():
        api.ime = form.ime_uporabnika.data
        api.izbor = form.izbor_SIEM.data
        api.api_key = form.api_kluc.data
        api.url = form.url.data
        api.barva = request.form.getlist('apiBarva')[0]
        api.admin_dostop = form.api_admin_dostop.data
        api.statistika = form.izdelava_statistike.data
        api.cas_spremljanja = form.cas_preverbe.data
        api.cas_opozorila = form.cas_opozorila.data
        db.session.commit()
        flash('uspešno si spremenil api', 'success')
        return redirect(url_for('apis.APIs'))
    elif request.method == 'GET':
        form.ime_uporabnika.data = api.ime
        form.izbor_SIEM.data = api.izbor
        form.api_kluc.data = api.api_key
        form.url.data = api.url
        barvica = api.barva
        form.api_admin_dostop.data = api.admin_dostop
        form.izdelava_statistike.data = api.statistika
        form.cas_preverbe.data = api.cas_spremljanja
        form.cas_opozorila.data = api.cas_opozorila
    return render_template('APIedit.html', title='API edit', name='Popravi API', form=form, barvica=barvica, legend='API edit')
    
@apis.route('/APIs/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def APIdelete(id):
    api_id = ApiModel.query.get_or_404(id)
    db.session.delete(api_id)
    db.session.commit()
    flash('zbrisu si en api iz seznama', 'success')
    return redirect(url_for('apis.APIs'))

