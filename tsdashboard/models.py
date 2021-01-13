from datetime import datetime

from flask import redirect, url_for
from flask_login import UserMixin, current_user
from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView

from tsdashboard import app, db, login_manager, ldap_manager, admin

# Declare a User Loader for Flask-Login.
# Simply returns the User if it exists in our 'database', otherwise
# returns None.
@login_manager.user_loader
def load_user(id):
    return UserModel.query.get(id)

@ldap_manager.save_user
def save_user(dn, username, data, memberships):
    check_user = UserModel.query.filter_by(dn=dn).first()
    if not check_user:
        new_user = UserModel(dn=dn, username=username, data=str(data), mail=data['mail'], pravice_id=0)
        db.session.add(new_user)
        db.session.commit()
        return new_user

    return check_user


offense_api_table = db.Table('offense_api',
    db.Column('offenseDB_id', db.Integer, db.ForeignKey('offense_model.id')),
    db.Column('apiDB_id', db.Integer, db.ForeignKey('api_model.id')))

offense_domain_table = db.Table('offense_domain',
    db.Column('offenseDB_id', db.Integer, db.ForeignKey('offense_model.id')),
    db.Column('qradardomain_id', db.Integer, db.ForeignKey('qradar_domain_model.id')))

offense_low_category = db.Table('offense_low_category',
    db.Column('offenseDB_id', db.Integer, db.ForeignKey('offense_model.id')),
    db.Column('qradarcategory_id', db.Integer, db.ForeignKey('qradar_category_low_model.name')))

offense_asigned_to = db.Table('offense_asigned_to',
    db.Column('offenseDB_id', db.Integer, db.ForeignKey('offense_model.id')),
    db.Column('qradaruser_id', db.Integer, db.ForeignKey('qradar_user_model.id')))

class UserModel(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    dn = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(30), nullable=False)
    data = db.Column(db.Text, nullable=False)
    mail = db.Column(db.String(255), nullable=False)
    ldapuser = db.Column(db.String(20), nullable=False, default='None')
    
    pravice_id = db.Column(db.Integer, db.ForeignKey('user_roles_model.id'), nullable=False)
    api_id = db.relationship('ApiModel', backref='juzername', lazy=True)

    def __repr__(self):
        return self.username

class UserRolesModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role_title = db.Column(db.String(20), nullable=False)
    role_privilegies = db.Column(db.String(60), nullable=False)
    user_id = db.relationship('UserModel', backref='juzer_pravice', lazy=True)

    def __repr__(self):
        return f"UserRole('{self.role_title}', '{self.role_privilegies}')"

class ApiModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ime = db.Column(db.String(50), nullable=False)
    izbor = db.Column(db.String(50), nullable=False)
    api_key = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(250), nullable=False)
    barva = db.Column(db.String(10), nullable=False)
    admin_dostop = db.Column(db.Boolean, nullable=False)
    statistika = db.Column(db.Boolean, nullable=False)
    cas_vnosa = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    cas_spremljanja = db.Column(db.Integer, nullable=False, default=0)
    cas_opozorila = db.Column(db.Integer, nullable=False, default=0)

    user_id = db.Column(db.String(30), db.ForeignKey('user_model.username'), nullable=False)
    domains = db.relationship('QradarDomainModel', backref='api_vnasalec', lazy=True) 

    def __repr__(self):
        return f"API(\
            '{self.ime}', '{self.izbor}', '{self.api_key}', \
            '{self.url}', '{self.barva }', '{self.admin_dostop}', \
            '{self.statistika}', '{self.cas_spremljanja}', '{self.cas_opozorila}', '{self.cas_vnosa}')"
    def __str__(self):
        return f"{self.ime}"

class QradarDomainModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    domain_id = db.Column(db.Integer, nullable=False)
    domain_name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    barva = db.Column(db.String(10))
    api_model_id = db.Column(db.Integer, db.ForeignKey('api_model.id'), nullable=False)

    def __repr__(self):
        return f"'{self.domain_id}', '{self.domain_name}', '{self.description}', '{self.api_model_id}', '{self.api_vnasalec}'"

class QradarCategoryLowModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cat_id = db.Column(db.Integer, default=0)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False, default="-")
    severity = db.Column(db.Integer, default=0)
    high_level_category_id = db.Column(db.Integer, nullable=False, default="-")
    high_cat = db.Column(db.Integer, db.ForeignKey('qradar_category_high_model.id'))

class QradarCategoryHighModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cat_id = db.Column(db.Integer)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    low_cat = db.relationship('QradarCategoryLowModel', backref='highCategory', lazy=True)

class QradarUserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, default="-")
    email = db.Column(db.String(255), nullable=False, default="-")

class OffenseModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    offense_id = db.Column(db.Integer)
    start_time = db.Column(db.Integer, default=0)
    close_time = db.Column(db.Integer)
    credibility = db.Column(db.Integer)
    relevance = db.Column(db.Integer)
    severity = db.Column(db.Integer)
    magnitude = db.Column(db.Integer)
    status = db.Column(db.String(10))
    event_count = db.Column(db.Integer)
    flow_count = db.Column(db.Integer)
    offense_type = db.Column(db.Integer)
    offense_source = db.Column(db.String(100))
    source_network = db.Column(db.String(20))

    od_api_id = db.relationship("ApiModel", secondary=offense_api_table, backref='api', lazy=True)
    od_qradardomene_id = db.relationship("QradarDomainModel", secondary=offense_domain_table, backref='qradardomain', lazy=True)
    assigned_to = db.relationship('QradarUserModel', secondary=offense_asigned_to, backref='asigned', lazy=True)
    categories = db.relationship('QradarCategoryLowModel', secondary=offense_low_category, backref='lowcat', lazy=True)

    def __repr__(self):
        return f"Offense('{self.offense_id}', '{self.start_time}')"



class Person(db.Model): pass
#     id = db.Column(db.Integer, primary_key=True)
#     addresses = db.relationship('Address', backref='person', lazy=True)

class Address(db.Model): pass
#     id = db.Column(db.Integer, primary_key=True)
#     person_id = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False)


class AppAdminIndexView(AdminIndexView): # pass # za spremembo /admin strani
    def is_accessible(self):
        return current_user.is_authenticated
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("users/login"))

class AppModelView(ModelView): #pass # za spremembo pogleda oz dostopa v /admin stran
    def is_accessible(self):
        return current_user.is_authenticated
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("users/login"))

admin._set_admin_index_view(index_view=AppAdminIndexView())

# flask-admin views
admin.add_view(AppModelView(UserModel, db.session))
admin.add_view(AppModelView(UserRolesModel, db.session))
admin.add_view(AppModelView(ApiModel, db.session))
admin.add_view(AppModelView(QradarDomainModel, db.session))
admin.add_view(AppModelView(QradarCategoryLowModel, db.session))
admin.add_view(AppModelView(QradarCategoryHighModel, db.session))
admin.add_view(AppModelView(QradarUserModel, db.session))
admin.add_view(AppModelView(OffenseModel, db.session))