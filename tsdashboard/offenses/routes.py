from datetime import datetime
import time

from flask import Blueprint, render_template, request, jsonify, make_response
from flask_login import login_required

from flask_socketio import send, emit

from tsdashboard import scheduler, socketio
from tsdashboard.models import ApiModel
from tsdashboard.utile.siem import Qradar, QradarConfig

offenses = Blueprint('offenses', __name__)

# VSI OFFENSE OD VSEH QRADARJEV
@offenses.route('/offenses')
@login_required 
def all_offenses():
    srch = Qradar('ALL')
    podatki = srch.getOffenses()
    legenda = srch.getLegenda()
    domene = srch.getDomains()
    
    return render_template('offenses.html', title='Offenses', name='Offenses', podatki=podatki, legenda=legenda, domene=domene)

# VSI OVENSI DOLOČENEGA API-JA
@offenses.route('/offenses/<int:apiId>')
@login_required
def offense_api(apiId):
    pass

# SPECIFIČEN OFFENSE
@offenses.route('/offenses/<int:apiId>/<int:offensId>')
@login_required
def offense(apiId, offensId):
    srch = Qradar()
    data = srch.getOffense(apiId, offensId)

    return render_template('offense.html', title=offensId, name='Offense ID', offens_id=offensId, data=data)

# OFFENSE OD POSAMEZNIKA
@offenses.route('/offenses/<string:username>')
@login_required
def offense_user(username):
    pass

# PREVERBA, ČE JE KAKŠEN NOV OFFENSE
@offenses.route('/offenses/_is_new', methods=["POST"])
@login_required
def offense_new():
    start = time.time()
    req = request.get_json()

    srch = Qradar("".format(req["siem"]))
    podatki = srch.getOffenses()

    res = make_response(jsonify(podatki), 200)
    end = time.time()
    print("pretečen čas", end, " - ",  start, " = ",  end - start)
    return res

@offenses.route('/offenses/_init', methods=["POST"])
@login_required
def offense_init():
    req = request.get_json()
    srch = Qradar("".format(req["siem"]))
    podatki = srch.getOffenses()
    legenda = srch.getLegenda()
    domene = srch.getDomains()
    res = make_response(jsonify({"legenda": legenda, "domene": domene, "podatki": podatki}), 200)

    return res

@socketio.on('message')
def handle_message(message):
    print('received message: ' + message)