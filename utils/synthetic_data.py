import random
from datetime import datetime, timedelta
import streamlit as st
from sqlalchemy import text


# --- Connection ---
@st.cache_resource
def get_conn():
    return st.connection("fitness", type="sql")


# --- Helpers ---
def random_datetime(start_days_ago=90):
    start = datetime.now() - timedelta(days=start_days_ago)
    delta = datetime.now() - start
    dt = start + timedelta(seconds=random.randint(0, int(delta.total_seconds())))
    return dt.date().isoformat(), dt.time().strftime("%H:%M:%S")


# --- Seed Measurements ---
def seed_measurements(n=50):
    conn = get_conn()
    with conn.session as session:
        for _ in range(n):
            date, time = random_datetime()
            session.execute(
                text("""
                    INSERT INTO Measurements
                    (date, time, weight, body_fat, waist, chest, shoulders, arms, thighs)
                    VALUES
                    (:date, :time, :weight, :body_fat, :waist, :chest, :shoulders, :arms, :thighs)
                """),
                {
                    "date": date,
                    "time": time,
                    "weight": round(random.uniform(70, 95), 1),
                    "body_fat": round(random.uniform(10, 25), 1),
                    "waist": round(random.uniform(75, 95), 1),
                    "chest": round(random.uniform(95, 115), 1),
                    "shoulders": round(random.uniform(110, 130), 1),
                    "arms": round(random.uniform(30, 40), 1),
                    "thighs": round(random.uniform(80, 100), 1),
                }
            )
        session.commit()
    print(f"Inserted {n} Measurements rows.")


# --- Seed Lifting ---
def seed_lifting(n=200):
    areas = ["Chest", "Back", "Legs", "Shoulders", "Arms"]
    exercises = {
        "Chest": ["Bench Press", "Incline Dumbbell Press", "Machine Chest Fly"],
        "Back": ["Lat Pulldown", "Pull Ups", "Dumbbell Row"],
        "Legs": ["Leg Extension", "Dumbbell Squat"],
        "Shoulders": ["Military Press", "Dumbbell Lateral Raise"],
        "Arms": ["Barbell Curl", "Hammer Curl"]
    }

    conn = get_conn()
    with conn.session as session:
        for _ in range(n):
            area = random.choice(areas)
            exercise = random.choice(exercises[area])
            date, time = random_datetime()
            set_number = random.randint(1, 5)
            reps = random.randint(5, 15)
            weight = round(random.uniform(20, 120), 1)
            volume = reps * weight
            rm = round(weight * (1 + reps / 30), 1)
            intensity = round(weight / rm * 100, 1)

            session.execute(
                text("""
                    INSERT INTO Lifting
                    (date, time, area, exercise, set_number, reps, weight,
                     volume, rm, intensity, notes)
                    VALUES
                    (:date, :time, :area, :exercise, :set_number, :reps, :weight,
                     :volume, :rm, :intensity, :notes)
                """),
                {
                    "date": date,
                    "time": time,
                    "area": area,
                    "exercise": exercise,
                    "set_number": set_number,
                    "reps": reps,
                    "weight": weight,
                    "volume": volume,
                    "rm": rm,
                    "intensity": intensity,
                    "notes": "auto-generated"
                }
            )
        session.commit()
    print(f"Inserted {n} Lifting rows.")


# --- Seed Cardio ---
def seed_cardio(n=100):
    activities = ["Run", "Bike", "Row", "Elliptical"]

    conn = get_conn()
    with conn.session as session:
        for _ in range(n):
            date, time = random_datetime()
            minutes = random.randint(10, 90)
            seconds = random.randint(0, 59)
            distance = round(random.uniform(2, 15), 2)
            pace = round((minutes + seconds / 60) / distance, 2)

            session.execute(
                text("""
                    INSERT INTO Cardio
                    (date, time, name, distance, minutes, seconds,
                     hr_avg, hr_max, pace, vo2_max,
                     anaerobic_time, aerobic_time, intensive_time, light_time,
                     aerobic_effect, anaerobic_effect, notes)
                    VALUES
                    (:date, :time, :name, :distance, :minutes, :seconds,
                     :hr_avg, :hr_max, :pace, :vo2_max,
                     :anaerobic_time, :aerobic_time, :intensive_time, :light_time,
                     :aerobic_effect, :anaerobic_effect, :notes)
                """),
                {
                    "date": date,
                    "time": time,
                    "name": random.choice(activities),
                    "distance": distance,
                    "minutes": minutes,
                    "seconds": seconds,
                    "hr_avg": random.randint(120, 160),
                    "hr_max": random.randint(160, 190),
                    "pace": pace,
                    "vo2_max": round(random.uniform(40, 60), 1),
                    "anaerobic_time": round(random.uniform(0, 10), 1),
                    "aerobic_time": round(random.uniform(10, 60), 1),
                    "intensive_time": round(random.uniform(5, 30), 1),
                    "light_time": round(random.uniform(5, 30), 1),
                    "aerobic_effect": round(random.uniform(1, 5), 1),
                    "anaerobic_effect": round(random.uniform(1, 5), 1),
                    "notes": "auto-generated"
                }
            )
        session.commit()
    print(f"Inserted {n} Cardio rows.")


# --- Main ---
if __name__ == "__main__":
    seed_measurements(50)
    seed_lifting(200)
    seed_cardio(100)
    print("Seeding completed.")
