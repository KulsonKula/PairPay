from flask import Blueprint, jsonify
from app.models import Bill

bill_bp = Blueprint('bill_bp', __name__)


@bill_bp.route('/api/bills', methods=['GET'])
def get_all_bills():
    try:
        bills = Bill.query.all()

        return jsonify([bill.to_dict() for bill in bills]), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify(message="An error occurred while retrieving bills.", error=str(e)), 500
