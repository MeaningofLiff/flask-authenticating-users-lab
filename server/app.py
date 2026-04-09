#!/usr/bin/env python3

#!/usr/bin/env python3

#!/usr/bin/env python3

from flask import Flask, request, session, jsonify
from flask_migrate import Migrate
from models import db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'super-secret-key'

db.init_app(app)
migrate = Migrate(app, db)


@app.post('/login')
def login():
    data = request.get_json()
    username = data.get('username')

    user = User.query.filter(User.username == username).first()

    if user:
        session['user_id'] = user.id
        return jsonify({
            "id": user.id,
            "username": user.username
        }), 200

    return jsonify({"error": "Unauthorized"}), 401


@app.delete('/logout')
def logout():
    session.pop('user_id', None)
    return '', 204


@app.get('/check_session')
def check_session():
    user_id = session.get('user_id')

    if user_id:
        # Modern SQLAlchemy 2.0 method
        user = db.session.get(User, user_id)
        if user:
            return jsonify({
                "id": user.id,
                "username": user.username
            }), 200

    # Must return an empty JSON object for the tests
    return jsonify({}), 401


if __name__ == '__main__':
    app.run(port=5555, debug=True) 