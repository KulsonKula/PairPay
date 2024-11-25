import logging
from flask import request
from flask_jwt_extended import get_jwt_identity
from app.models import Log
import time
from app import db
from sqlalchemy import func
from functools import wraps

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def make_log_wrapper(func):
    @wraps(func)
    def wrapper_fc(*args, **kwargs):
        jwt_identity = get_jwt_identity()
        endpoint = request.path
        t1 = time.time()
        response = func(*args, **kwargs)
        t2 = time.time()

        log_data = f"wywołał endpoint: {endpoint}, status: {response[1]}, wynik: {response[0]}, czas:{t2-t1:.4f}s"
        create_log(jwt_identity, log_data)

        return response
    return wrapper_fc


def serialize_bill(bill):
    return {
        "id": bill.id,
        "user_creator_id": bill.user_creator_id,
        "name": bill.name,
        "label": bill.label,
        "status": bill.status,
        "total_sum": bill.total_sum,
        "created_at": bill.created_at,
        "users": [user.id for user in bill.users]
    }


def create_log(user_id, data):
    log = Log(user_id=user_id, data=data, created_at=func.now())
    db.session.add(log)
    db.session.commit()
