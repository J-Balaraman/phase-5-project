import os
from flask import request, jsonify, session
from config import app, db, jwt
from models import User, WorkoutRoutine, ExerciseLog, UserMetrics, UserWorkoutRoutine
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from functools import wraps

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

SECRET_KEY = '1850980026'

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('x-access-token')
        if not token:
            return jsonify({"message": "Token is missing!"}), 401
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            current_user = User.query.filter_by(id=data['user_id']).first()
        except Exception as e:
            return jsonify({"message": "Token is invalid!"}), 401
        return f(current_user, *args, **kwargs)
    return decorated

def generate_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(days=1)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

@app.route('/')
def index():
    return '<h1>Phase 5 Project Server</h1>'

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    email = data['email']
    password = data['password']

    if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
        return jsonify({"message": "Username or email already exists"}), 400

    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    new_user = User(username=username, email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data['email']
    password = data['password']

    user = User.query.filter_by(email=email).first()

    if user and check_password_hash(user.password, password):
        token = generate_token(user.id)
        user_data = {
            "username": user.username,
            "email": user.email,
            "active_workout_id": user.active_workout_id,
            "workout_routines": [routine.name for routine in user.workout_routines],
            "exercise_logs": [log.description for log in user.exercise_logs],
            "user_metrics": [{"date": metric.date.isoformat(), "weight": metric.weight, "body_fat": metric.body_fat} for metric in user.user_metrics]
        }
        return jsonify({
            "message": "Logged in successfully",
            "user": user_data,
            "token": token
        }), 200

    return jsonify({"message": "Invalid email or password"}), 401

@app.route('/dashboard', methods=['GET'])
def dashboard():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"message": "Not authenticated"}), 401

    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    active_workout = WorkoutRoutine.query.filter_by(id=user.active_workout_id).first() if user.active_workout_id else None
    workout_data = {
        "id": active_workout.id,
        "name": active_workout.name,
        "exercises": [{"name": exercise.name, "description": exercise.description, "reps": exercise.reps, "sets": exercise.sets, "duration": exercise.duration} for exercise in active_workout.exercises]
    } if active_workout else {}

    exercise_logs = [{"id": log.id, "description": log.description, "timestamp": log.timestamp.isoformat()} for log in user.exercise_logs]
    user_metrics = [{"date": metric.date.isoformat(), "weight": metric.weight, "body_fat": metric.body_fat} for metric in user.user_metrics]

    return jsonify({
        "message": "Dashboard data",
        "active_workout": workout_data,
        "exercise_logs": exercise_logs,
        "user_metrics": user_metrics
    })

@app.route('/user_metrics', methods=['GET', 'POST', 'DELETE'])
@token_required
def user_metrics(current_user):
    if request.method == 'GET':
        user_metrics = UserMetrics.query.filter_by(user_id=current_user.id).all()
        result = [{"id": metric.id, "date": metric.date.isoformat(), "weight": metric.weight, "body_fat": metric.body_fat} for metric in user_metrics]
        return jsonify(result)

    elif request.method == 'POST':
        data = request.get_json()
        date = datetime.fromisoformat(data['date']).date()
        weight = data['weight']
        body_fat = data['body_fat']

        new_metric = UserMetrics(user_id=current_user.id, date=date, weight=weight, body_fat=body_fat)
        db.session.add(new_metric)
        db.session.commit()
        return jsonify({"id": new_metric.id, "date": new_metric.date.isoformat(), "weight": new_metric.weight, "body_fat": new_metric.body_fat})

    elif request.method == 'DELETE':
        data = request.get_json()
        metric_id = data.get('id')

        if not metric_id:
            return jsonify({"message": "Metric ID is required"}), 400

        metric = UserMetrics.query.filter_by(id=metric_id, user_id=current_user.id).first()
        if not metric:
            return jsonify({"message": "Metric not found"}), 404

        db.session.delete(metric)
        db.session.commit()
        return jsonify({"message": "Metric deleted successfully"}), 200


@app.route('/user_metrics/<int:metric_id>', methods=['DELETE'])
@token_required
def delete_user_metric(current_user, metric_id):
    metric = UserMetrics.query.filter_by(id=metric_id, user_id=current_user.id).first()
    if not metric:
        return jsonify({"message": "Metric not found"}), 404

    db.session.delete(metric)
    db.session.commit()
    return jsonify({"message": "Metric deleted successfully"}), 200

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
