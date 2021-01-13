from flask import Blueprint

from flask import Flask, url_for, render_template, redirect, request, render_template_string
from flask_login import login_required, logout_user, login_user
from flask_ldap3_login.forms import LDAPLoginForm

from tsdashboard import db, login_manager, ldap_manager
from tsdashboard.models import UserModel, ApiModel
from tsdashboard.utile.siem import Qradar

users = Blueprint('users', __name__)

@users.route('/manual_login')
def manual_login():
    app.ldap3_login_manager.authenticate('username', 'password')

@users.route('/login', methods=['GET', 'POST'])
def login():
    template = """
    {{ get_flashed_messages() }}
    {{ form.errors }}
    <form method="POST">
        <label>Username{{ form.username() }}</label>
        <label>Password{{ form.password() }}</label>
        {{ form.submit() }}
        {{ form.hidden_tag() }}
    </form>
    """
    form = LDAPLoginForm()

    if form.validate_on_submit():
        # Successfully logged in, We can now access the saved user object via form.user.
        login_user(form.user)  # Tell flask-login to log them in.
        next_page = request.args.get('next')
        return redirect(next_page) if next_page else redirect(url_for('main.home'))
        # return redirect('/')  # Send them home

    return render_template_string(template, form=form)

@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@users.route('/profil/<username>')
@login_required
def profil(username):
    return render_template('profil.html', title='Profil', name='Profil', data=username)

@users.route('/user/test')
def testfunc():
    srch = Qradar()
    data = srch.getUserAdmin()

    return render_template('test.html', title="user test", name='user test', data=data)