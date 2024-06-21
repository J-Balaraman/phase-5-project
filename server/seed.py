from random import randint, choice as rc
from app import app
from models import db, User, WorkoutRoutine, ExerciseLog, UserMetrics
from werkzeug.security import generate_password_hash

def create_users():
    users = [
        User(username="john_doe", email="john@example.com", password=generate_password_hash("password123", method='pbkdf2:sha256')),
        User(username="jane_smith", email="jane@example.com", password=generate_password_hash("password456", method='pbkdf2:sha256'))
    ]
    return users

def create_workout_routines():
    routines = [
        WorkoutRoutine(
            name="Full Body Workout",
            description="A full body workout routine",
            sunday="Rest",
            monday="Squats, Deadlifts",
            tuesday="Bench Press, Rows",
            wednesday="Rest",
            thursday="Overhead Press, Pull-ups",
            friday="Rest",
            saturday="Cardio"
        ),
        WorkoutRoutine(
            name="Push Pull Legs",
            description="A push pull legs routine",
            sunday="Push: Bench Press, Overhead Press",
            monday="Pull: Deadlifts, Rows",
            tuesday="Legs: Squats, Lunges",
            wednesday="Rest",
            thursday="Push: Bench Press, Overhead Press",
            friday="Pull: Deadlifts, Rows",
            saturday="Legs: Squats, Lunges"
        )
    ]
    return routines

def create_exercise_logs(users):
    logs = [
        ExerciseLog(user_id=users[0].id, date="2023-01-01", description="Squats, Deadlifts"),
        ExerciseLog(user_id=users[0].id, date="2023-01-02", description="Bench Press, Rows")
    ]
    return logs

def create_user_metrics(users):
    metrics = [
        UserMetrics(user_id=users[0].id, date="2023-01-01", weight=70.0, body_fat=15.0),
        UserMetrics(user_id=users[0].id, date="2023-01-02", weight=70.5, body_fat=14.8)
    ]
    return metrics

if __name__ == '__main__':
    with app.app_context():
        print("Clearing db...")
        db.drop_all()
        db.create_all()

        print("Seeding users...")
        users = create_users()
        db.session.add_all(users)
        db.session.commit()

        print("Seeding workout routines...")
        routines = create_workout_routines()
        db.session.add_all(routines)
        db.session.commit()

        print("Seeding exercise logs...")
        logs = create_exercise_logs(users)
        db.session.add_all(logs)
        db.session.commit()

        print("Seeding user metrics...")
        metrics = create_user_metrics(users)
        db.session.add_all(metrics)
        db.session.commit()

        print("Done seeding!")
