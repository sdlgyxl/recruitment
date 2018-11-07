from flask import Blueprint

bp = Blueprint('main', __name__)

from .user import views as userview
userview.rp.register(bp)

from app.main import views
