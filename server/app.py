import os
from flask import request, jsonify, session
from config import app, db, api
from models import User, WorkoutRoutine, ExerciseLog, UserMetrics, UserWorkoutRoutine
from werkzeug.security import generate_password_hash, check_password_hash

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

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
        session['user_id'] = user.id
        user_data = {
            "username": user.username,
            "email": user.email,
            "active_workout_id": user.active_workout_id,
            "workout_routines": [routine.name for routine in user.workout_routines],
            "exercise_logs": [log.description for log in user.exercise_logs],
            "user_metrics": [{"date": metric.date, "weight": metric.weight, "body_fat": metric.body_fat} for metric in user.user_metrics]
        }
        return jsonify({
            "message": "Logged in successfully",
            "user": user_data,
            "token": "your_token_here"  # You might want to generate a token if using JWT or other methods
        }), 200

    return jsonify({"message": "Invalid email or password"}), 401


@app.route('/dashboard', methods=['GET'])
def dashboard():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"message": "Not authenticated"}), 401

    user = User.query.get(user_id)
    return jsonify({
        "username": user.username,
        "email": user.email,
        "active_workout_id": user.active_workout_id,
        "workout_routines": [routine.name for routine in user.workout_routines],
        "exercise_logs": [log.description for log in user.exercise_logs],
        "user_metrics": [{"date": metric.date, "weight": metric.weight, "body_fat": metric.body_fat} for metric in user.user_metrics]
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

@app.route('/workouts/<int:workout_id>', methods=['GET', 'POST'])
def workouts_by_id(workout_id):
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
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({"message": "Not authenticated"}), 401

        user = User.query.get(user_id)
        user.workout_routines.append(workout)
        db.session.commit()
        return jsonify({"message": "Workout added to user successfully"}), 201

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
def user_logs():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"message": "Not authenticated"}), 401

    if request.method == 'GET':
        logs = ExerciseLog.query.filter_by(user_id=user_id).all()
        return jsonify([{"id": log.id, "date": log.date, "description": log.description} for log in logs]), 200

    if request.method == 'POST':
        data = request.get_json()
        new_log = ExerciseLog(user_id=user_id, date=data['date'], description=data['description'])
        db.session.add(new_log)
        db.session.commit()
        return jsonify({"message": "Log created successfully"}), 201

    if request.method == 'PATCH':
        data = request.get_json()
        log = ExerciseLog.query.get(data['id'])
        if log.user_id != user_id:
            return jsonify({"message": "Not authorized"}), 403

        log.date = data['date']
        log.description = data['description']
        db.session.commit()
        return jsonify({"message": "Log updated successfully"}), 200

    if request.method == 'DELETE':
        data = request.get_json()
        log = ExerciseLog.query.get(data['id'])
        if log.user_id != user_id:
            return jsonify({"message": "Not authorized"}), 403

        db.session.delete(log)
        db.session.commit()
        return jsonify({"message": "Log deleted successfully"}), 200

@app.route('/user_graph', methods=['GET'])
def user_graph():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"message": "Not authenticated"}), 401

    metrics = UserMetrics.query.filter_by(user_id=user_id).all()
    return jsonify([{"date": metric.date, "weight": metric.weight, "body_fat": metric.body_fat} for metric in metrics]), 200

if __name__ == '__main__':
    app.run(port=5000, debug=True)
