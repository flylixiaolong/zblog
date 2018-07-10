from flask import Blueprint, render_template, request, flash, redirect
from flask_login import login_user
from blog.models import Admin
from blog import db
