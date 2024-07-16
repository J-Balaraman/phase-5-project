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
            WorkoutRoutine(
                name='Full Body Workout',
                description='A comprehensive workout routine targeting all major muscle groups, promoting overall strength and conditioning. Each day focuses on different muscle groups with adequate rest days for recovery.',
                sunday='Rest day to allow for full body recovery.',
                monday='Leg day: Squats, Deadlifts, Lunges, Leg Press, Calf Raises.',
                tuesday='Arm day: Bicep Curls, Tricep Dips, Hammer Curls, Tricep Extensions, Forearm Curls.',
                wednesday='Rest day to allow muscle recovery and growth.',
                thursday='Chest day: Bench Press, Incline Dumbbell Press, Chest Flyes, Push-ups, Chest Dips.',
                friday='Back day: Pull-Ups, Bent Over Rows, Deadlifts, Lat Pulldowns, T-Bar Rows.',
                saturday='Rest day to ensure muscle recovery.'
            ),
            WorkoutRoutine(
                name='Upper Body Workout',
                description='Focuses on building strength and muscle in the upper body, including the chest, back, shoulders, and arms. This routine ensures balanced development and strength gains.',
                sunday='Rest day for recovery.',
                monday='Chest: Bench Press, Incline Dumbbell Press, Cable Crossovers, Push-ups.',
                tuesday='Back: Deadlifts, Pull-Ups, Bent Over Rows, One-Arm Dumbbell Rows.',
                wednesday='Rest day for recovery.',
                thursday='Arms: Bicep Curls, Tricep Dips, Hammer Curls, Skull Crushers.',
                friday='Shoulders: Overhead Press, Lateral Raises, Front Raises, Shrugs.',
                saturday='Rest day for muscle recovery.'
            ),
            WorkoutRoutine(
                name='Lower Body Workout',
                description='Dedicated to building strength and endurance in the lower body, focusing on the legs and glutes. This routine is ideal for athletes and individuals looking to enhance lower body power.',
                sunday='Rest day for full recovery.',
                monday='Legs: Squats, Leg Press, Lunges, Hamstring Curls, Calf Raises.',
                tuesday='Legs: Deadlifts, Bulgarian Split Squats, Step-Ups, Leg Extensions.',
                wednesday='Rest day for recovery.',
                thursday='Legs: Squats, Glute Bridges, Romanian Deadlifts, Calf Raises.',
                friday='Legs: Leg Press, Walking Lunges, Hamstring Curls, Seated Calf Raises.',
                saturday='Rest day to allow muscle recovery.'
            ),
            WorkoutRoutine(
                name='Cardio Workout',
                description='Designed to improve cardiovascular health and endurance, this routine includes a variety of cardio exercises to keep the heart rate up and burn calories.',
                sunday='Running: Long-distance running at a steady pace for endurance.',
                monday='Biking: Interval training with sprints and steady-state biking.',
                tuesday='Swimming: Freestyle, Backstroke, and Interval Training.',
                wednesday='Running: Tempo runs with a mix of fast and slow paces.',
                thursday='Biking: Hill climbs and interval sprints.',
                friday='Swimming: Distance swimming with focus on technique and endurance.',
                saturday='Rest day to allow the body to recover from cardio activities.'
            )
        ]
        db.session.bulk_save_objects(workout_routines)
        db.session.commit()

def seed_exercise_logs():
    with app.app_context():
        start_date = date(2024, 1, 1)
        exercise_logs = []
        descriptions = [
            'Squats, Deadlifts, and Lunges with increasing weights and reps.',
            'Bench Press, Dumbbell Press, and Cable Crossovers with varied sets.',
            'Running on the treadmill, followed by a cycling session.',
            'Bicep Curls, Tricep Extensions, and Hammer Curls with supersets.',
            'Pull-Ups, Bent Over Rows, and Lat Pulldowns with pyramid sets.',
            'Leg Press, Calf Raises, and Hamstring Curls focusing on endurance.',
            'Interval running with sprints and steady pace cycling for endurance.',
            'Swimming with mixed strokes and interval training for cardio strength.',
            'Chest Flyes, Push-ups, and Dips with high-intensity circuits.',
            'Back Extensions, T-Bar Rows, and Deadlifts with varied intensities.'
        ]
        for i in range(10):
            exercise_logs.extend([
                {"user_id": 1, "date": start_date + timedelta(days=i), "description": random.choice(descriptions)},
                {"user_id": 2, "date": start_date + timedelta(days=i), "description": random.choice(descriptions)},
                {"user_id": 3, "date": start_date + timedelta(days=i), "description": random.choice(descriptions)}
            ])
        db.session.bulk_insert_mappings(ExerciseLog, exercise_logs)
        db.session.commit()

def seed_user_metrics():
    with app.app_context():
        start_date = date(2024, 1, 1)
        user_metrics = []
        for i in range(10):
            user_metrics.extend([
                UserMetrics(user_id=1, date=start_date + timedelta(days=i), weight=round(150 + random.uniform(-2, 2), 2), body_fat=round(20 - random.uniform(0, 0.5), 2)),
                UserMetrics(user_id=2, date=start_date + timedelta(days=i), weight=round(160 + random.uniform(-2, 2), 2), body_fat=round(18 - random.uniform(0, 0.5), 2)),
                UserMetrics(user_id=3, date=start_date + timedelta(days=i), weight=round(140 + random.uniform(-2, 2), 2), body_fat=round(22 - random.uniform(0, 0.5), 2))
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
