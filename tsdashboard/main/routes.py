from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/domov')
@main.route('/index')
@main.route('/home')

# @login_required
def home():
    return render_template('home.html', title='Home', name='Dom')

@main.route('/about') 
def about():
    return render_template('about.html', title='About', name='About')
