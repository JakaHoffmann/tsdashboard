from flask import Blueprint, render_template, redirect, url_for, jsonify, make_response
from flask_login import login_required, current_user

from tsdashboard.models import OffenseModel, ApiModel, QradarDomainModel
from tsdashboard.utile.siem import Qradar, QradarConfig, QradarStat

stats = Blueprint('stats', __name__)

@stats.route('/stats')
@login_required
def statistika():
    userData = QradarStat('user', 3)
    catData = QradarStat('cat', 3)

    user_podatki = userData.userData()
    cat_podatki = catData.catData()
    return render_template('stats.html', title='Statistika', name='Statistika', user_podatki=user_podatki, cat_podatki=cat_podatki)

@stats.route('/stats/_userdata', methods=["POST"])
@login_required
def statUserData():
    userData = QradarStat('user', 3)
    user_podatki = userData.userData()
    print(user_podatki)
    res = make_response(user_podatki, 200)
    return res

@stats.route('/stats/_catdata', methods=["POST"])
@login_required
def statCatData():
    req = request.get_json()
    catData = QradarStat('cat', 3)
    cat_podatki = jsonify(catData.catData())
    res = make_response(jsonify(cat_podatki), 200)
    return res

@stats.route('/stats/user/<string:username>')
@login_required
def stats_for_username(username):
    if current_user is username:
        return redirect(url_for("users.profil", username=username))
    else:
        return render_template('userstats.html', title='Statistika', name='Statistika - ' + username, username=username)

@stats.route('/stats/cat/<string:category>')
@login_required
def stats_for_category(category):
    return render_template('catstats.html', title='Statistika', name='Statistika - ' + category, category=category)