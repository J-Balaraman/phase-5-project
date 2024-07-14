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
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return jsonify({"message": "Bearer token malformed"}), 401
        
        if not token:
            return jsonify({"message": "Token is missing!"}), 401
        
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            current_user = User.query.filter_by(id=data['user_id']).first()
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token has expired!"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Invalid token!"}), 401
        
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
        token = jwt.encode({
            'user_id': user.id,
            'exp': datetime.utcnow() + timedelta(days=1)
        }, SECRET_KEY, algorithm='HS256')
        
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
@token_required
def dashboard(current_user):
    active_workout_name = None
    if current_user.active_workout_id:
        active_workout = WorkoutRoutine.query.filter_by(id=current_user.active_workout_id).first()
        active_workout_name = active_workout.name if active_workout else None

    workout_routines = [{"id": routine.id, "name": routine.name} for routine in current_user.workout_routines]
    exercise_logs = [{"id": log.id, "description": log.description, "date": log.date.isoformat()} for log in current_user.exercise_logs]
    user_metrics = [{"date": metric.date.isoformat(), "weight": metric.weight, "body_fat": metric.body_fat} for metric in current_user.user_metrics]

    return jsonify({
        "username": current_user.username,
        "email": current_user.email,
        "active_workout": active_workout_name,
        "workout_routines": workout_routines,
        "exercise_logs": exercise_logs,
        "user_metrics": user_metrics
    }), 200

@app.route('/workouts', methods=['GET', 'POST'])
def workouts():
    if request.method == 'GET':
        workouts = WorkoutRoutine.query.all()
        return jsonify([{"id": workout.id, "name": workout.name, "description": workout.description} for workout in workouts]), 200

    if request.method == 'POST':
        data = request.get_json()
        new_workout = WorkoutRoutine(
            name=data['name'],
            description=data['description'],
            sunday=data['sunday'],
            monday=data['monday'],
            tuesday=data['tuesday'],
            wednesday=data['wednesday'],
            thursday=data['thursday'],
            friday=data['friday'],
            saturday=data['saturday']
        )
        db.session.add(new_workout)
        db.session.commit()
        return jsonify({"message": "Workout created successfully"}), 201

@app.route('/workouts/<int:workout_id>', methods=['GET', 'POST', 'PATCH', 'DELETE'])
@token_required
def workouts_by_id(current_user, workout_id):
    workout = WorkoutRoutine.query.get(workout_id)
    if not workout:
        return jsonify({"message": "Workout not found"}), 404

    if request.method == 'GET':
        return jsonify({
            "id": workout.id,
            "name": workout.name,
            "description": workout.description,
            "sunday": workout.sunday,
            "monday": workout.monday,
            "tuesday": workout.tuesday,
            "wednesday": workout.wednesday,
            "thursday": workout.thursday,
            "friday": workout.friday,
            "saturday": workout.saturday
        }), 200

    if request.method == 'POST':
        user = User.query.get(current_user.id)
        user.workout_routines.append(workout)
        db.session.commit()
        return jsonify({"message": "Workout added to user successfully"}), 201

    if request.method == 'PATCH':
        user = User.query.get(current_user.id)
        user.active_workout_id = workout_id
        db.session.commit()
        return jsonify({"message": "Workout set as active successfully"}), 200
    
    if request.method == 'DELETE':
        user = User.query.get(current_user.id)
        user_workout = UserWorkoutRoutine.query.filter_by(user_id=current_user.id, workout_routine_id=workout_id).first()
        if user_workout:
            db.session.delete(user_workout)
            db.session.commit()
            return jsonify({"message": "Workout removed from user successfully"}), 200
        else:
            return jsonify({"message": "Workout not found in user's routines"}), 404

@app.route('/create_workout', methods=['POST'])
def create_workout():
    data = request.get_json()
    new_workout = WorkoutRoutine(
            name=data['name'],
            description=data['description'],
            sunday=data['sunday'],
            monday=data['monday'],
            tuesday=data['tuesday'],
            wednesday=data['wednesday'],
            thursday=data['thursday'],
            friday=data['friday'],
            saturday=data['saturday']
        )
    db.session.add(new_workout)
    db.session.commit()
    return jsonify({"message": "Workout created successfully"}), 201

@app.route('/user_logs', methods=['GET', 'POST', 'PATCH', 'DELETE'])
@token_required
def user_logs(current_user):
    if request.method == 'GET':
        logs = ExerciseLog.query.filter_by(user_id=current_user.id).all()
        return jsonify([{"id": log.id, "date": log.date.isoformat(), "description": log.description} for log in logs]), 200

    if request.method == 'POST':
        data = request.get_json()
        data["date"] = datetime.strptime(data["date"], "%Y-%m-%d").date()
        new_log = ExerciseLog(user_id=current_user.id, date=data['date'], description=data['description'])
        db.session.add(new_log)
        db.session.commit()
        return jsonify({"message": "Log created successfully"}), 201

    if request.method == 'PATCH':
        data = request.get_json()
        log_id = data['id']
        new_date = data['date']
        new_description = data['description']

        if new_date:
            new_date = datetime.strptime(new_date, '%Y-%m-%d').date()

        log = ExerciseLog.query.get(log_id)
        if new_date:
            log.date = new_date
        if new_description:
            log.description = new_description
        db.session.commit()
        return jsonify({"message": "Log updated successfully"}), 200

    if request.method == 'DELETE':
        data = request.get_json()
        log = ExerciseLog.query.get(data['id'])
        if log.user_id != current_user.id:
            return jsonify({"message": "Not authorized"}), 403

        db.session.delete(log)
        db.session.commit()
        return jsonify({"message": "Log deleted successfully"}), 200


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
