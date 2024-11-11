from app import create_app

from flask import Flask, jsonify
from app import create_app, get_db_engine
from sqlalchemy.exc import OperationalError

app = create_app()


# This route is used to test DB connection
@app.route('/test-db', methods=['GET'])
def test_db_connection():
    try:
        engine = get_db_engine(app)

        # Try to connect to the database and execute a simple query
        with engine.connect() as connection:
            connection.execute("SELECT 1")  # Simple query to check connection

        return jsonify(message="Database is connected and working properly."), 200

    except OperationalError as e:
        # Handle connection error
        return jsonify(message="Database connection failed.", error=str(e)), 500


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
