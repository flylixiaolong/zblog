from flask import Blueprint, render_template
from flask_login import login_user

admin = Blueprint('admin', __name__, url_prefix='/admin', template_folder='templates')


@admin.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('admin/login.html')