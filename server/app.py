import os
from flask import request
from config import app, db, api, jsonify
from models import User, WorkoutRoutine, ExerciseLog, UserMetrics, UserWorkoutRoutine

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'library.db')}")

@app.route('/')
def index():
    return '<h1>Phase 5 Project Sample Text</h1>'

@app.route('/register', methods=['POST'])
def register():
# user can create a new account

@app.route('/login', methods=['POST'])
def login():
# user can log into an existing account

@app.route('/dashboard', methods=['GET'])
def dashboard():
# user can view their data

@app.route('/workouts', methods=['GET', 'POST'])
def workouts():
# user can view all workouts in database and add them to their list

@app.route('/workouts/<int>', methods=['GET', 'POST'])
def workouts_by_id():
# user can view more details on a specific workout and add it to their list

@app.route('/create_workout', methods=['POST'])
def create_workout():
# user can create workouts to add to database

@app.route('/user_logs', methods=['GET', 'POST', 'PATCH', 'DELETE'])
def user_logs():
# user can view their workout logs, create new ones, update old ones, and delete old ones

@app.route('/user_graph', methods=['GET'])
def user_graph():
# user can view their data plotted on a graph to show progress

if __name__ == '__main__':
    app.run(port=5555, debug=True)

