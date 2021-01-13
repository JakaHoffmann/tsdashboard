from flask import Flask, url_for, render_template
from flask_ldap3_login import LDAP3LoginManager
from flask_login import LoginManager, login_user, UserMixin, current_user, login_required, logout_user
from flask import render_template_string, redirect, request
from flask_ldap3_login.forms import LDAPLoginForm

from tsdashboard import app, db, login_manager, ldap_manager
from tsdashboard.models import UserModel, ApiModel


# Declare some routes for usage to show the authentication process.

import requests

@app.route('/test')
def testis():
    _connection = requests.Session()
    odgovor = {}
    glava = {'X-Arbux-APIToken': 'ZcbMhc2YdVfJ8yLg'}

    try:
        with _connection as s:
            r = s.get("<test_url>", headers=glava)
            r.raise_for_status()
        odgovor = r.json()
    except requests.exceptions.HTTPError as err:
        print("ERROR HTTP: {}".format(err))
        if r.status_code == requests.codes.forbidden:
            print("403 403 403")
    except requests.exceptions.ConnectionError as errc:
        print ("ERROR CONNECTING': {}".format(errc))
    
    except requests.exceptions.ProxyError as errp:
        print ("ERROR PROXY': {}".format(errp))
    except requests.exceptions.SSLError as errs:
        print ("ERROR SSL': {}".format(errs))
    except requests.exceptions.InvalidURL as erriur:
        print ("ERROR INVALID URL': {}".format(erriur))
    except requests.exceptions.InvalidHeader as errh:
        print ("ERROR INVALID HEADER': {}".format(errh))
    
    return odgovor
