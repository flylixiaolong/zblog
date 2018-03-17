from .models import Admin
from sqlalchemy import event
from werkzeug.security import generate_password_hash


@event.listens_for(Admin.password, 'set', retval=True)
def password_hash(target, value, oldvalue, initiator):
    return generate_password_hash(value)
    