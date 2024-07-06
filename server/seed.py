from datetime import date, timedelta
import random
from app import app, db
from models import User, WorkoutRoutine, ExerciseLog, UserMetrics, UserWorkoutRoutine
from werkzeug.security import generate_password_hash

def clear_db():
    with app.app_context():
        db.drop_all()
        db.create_all()

def seed_users():
    with app.app_context():
        users = [
            User(username='jdoe', email='jdoe@example.com', password=generate_password_hash('password', method='pbkdf2:sha256')),
            User(username='asmith', email='asmith@example.com', password=generate_password_hash('password', method='pbkdf2:sha256')),
            User(username='mjane', email='mjane@example.com', password=generate_password_hash('password', method='pbkdf2:sha256'))
        ]
        db.session.bulk_save_objects(users)
        db.session.commit()

def seed_workout_routines():
    with app.app_context():
        workout_routines = [
            WorkoutRoutine(name='Full Body Workout', description='A complete full body workout', sunday='Rest', monday='Legs', tuesday='Arms', wednesday='Rest', thursday='Chest', friday='Back', saturday='Rest'),
            WorkoutRoutine(name='Upper Body Workout', description='Upper body focus', sunday='Rest', monday='Chest', tuesday='Back', wednesday='Rest', thursday='Arms', friday='Shoulders', saturday='Rest'),
            WorkoutRoutine(name='Lower Body Workout', description='Lower body focus', sunday='Rest', monday='Legs', tuesday='Legs', wednesday='Rest', thursday='Legs', friday='Legs', saturday='Rest'),
            WorkoutRoutine(name='Cardio Workout', description='Cardio exercises', sunday='Running', monday='Biking', tuesday='Swimming', wednesday='Running', thursday='Biking', friday='Swimming', saturday='Rest')
        ]
        db.session.bulk_save_objects(workout_routines)
        db.session.commit()

def seed_exercise_logs():
    with app.app_context():
        start_date = date(2024, 1, 1)
        exercise_logs = []
        for i in range(10):
            exercise_logs.extend([
                {"user_id": 1, "date": start_date + timedelta(days=i), "description": 'Squats, Deadlifts'},
                {"user_id": 2, "date": start_date + timedelta(days=i), "description": 'Bench Press, Rows'},
                {"user_id": 3, "date": start_date + timedelta(days=i), "description": 'Running, Biking'}
            ])
        db.session.bulk_insert_mappings(ExerciseLog, exercise_logs)
        db.session.commit()

def seed_user_metrics():
    with app.app_context():
        start_date = date(2024, 1, 1)
        user_metrics = []
        for i in range(10):
            user_metrics.extend([
                UserMetrics(user_id=1, date=start_date + timedelta(days=i), weight=150 + i, body_fat=20 - i*0.1),
                UserMetrics(user_id=2, date=start_date + timedelta(days=i), weight=160 + i, body_fat=18 - i*0.1),
                UserMetrics(user_id=3, date=start_date + timedelta(days=i), weight=140 + i, body_fat=22 - i*0.1)
            ])
        db.session.bulk_save_objects(user_metrics)
        db.session.commit()

def seed_user_workout_routines():
    with app.app_context():
        user_workout_routine_link = [
            UserWorkoutRoutine(user_id=1, workout_routine_id=1),
            UserWorkoutRoutine(user_id=2, workout_routine_id=2),
            UserWorkoutRoutine(user_id=3, workout_routine_id=3)
        ]
        db.session.bulk_save_objects(user_workout_routine_link)
        db.session.commit()

if __name__ == '__main__':
    print("Clearing db...")
    clear_db()
    print("Seeding users...")
    seed_users()
    print("Seeding workout routines...")
    seed_workout_routines()
    print("Seeding exercise logs...")
    seed_exercise_logs()
    print("Seeding user metrics...")
    seed_user_metrics()
    print("Seeding user workout routines...")
    seed_user_workout_routines()
    print("Done!")
