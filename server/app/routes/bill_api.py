from flask import Blueprint, jsonify, current_app
from app.models import Bill

bill_bp = Blueprint('bill_bp', __name__)

# TODO pw do przetestowania tylko


@bill_bp.route('/api/bills', methods=['GET'])
def get_all_bills():
    db = current_app.db
    session = db.get_session()
    try:
        bills = session.query(Bill).all()
        return jsonify([bill.to_dict() for bill in bills]), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify(message="An error occurred while retrieving bills.", error=str(e)), 500
    finally:
        session.close()
