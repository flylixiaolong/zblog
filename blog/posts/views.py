from flask import Blueprint, render_template, request, flash, redirect
from flask_login import login_user
from blog.models import Admin
from blog import db

posts = Blueprint('posts', __name__, url_prefix='/posts', template_folder='templates')