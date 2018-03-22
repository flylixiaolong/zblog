from flask import Blueprint, render_template, request, flash
from flask_login import login_user
from blog.models import Admin
from blog import db

admin = Blueprint('admin', __name__, url_prefix='/admin', template_folder='templates')


@admin.route('/login', methods=['GET', 'POST'])
def login():
    if(request.method=='POST'):
        user_name = request.form['user_name']
        password = request.form['password']
        user = db.session.query(Admin).filter(Admin.user_name==user_name).one_or_none()
        if(user and user.verify_password(password)):
            login_user(user)
            return '<p> hello you! <p>'
        flash('Invalid username or password.')
    return render_template('admin/login.html')
        