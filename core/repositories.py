import streamlit as st
from sqlalchemy import text
from core.db import get_conn

def insert_cardio(data: dict):
    conn = get_conn()

    date = data["date"]
    time = data["time"]
    name = data["name"]
    distance = data["distance"]
    minutes = data["minutes"]
    seconds = data["seconds"]
    hr_avg = data["hr_avg"]
    hr_max = data["hr_max"]
    pace = data["pace"]
    vo2_max = data["vo2_max"]
    anaerobic_time = data["anaerobic_time"]
    aerobic_time = data["aerobic_time"]
    intensive_time = data["intensive_time"]
    light_time = data["light_time"]
    aerobic_effect = data["aerobic_effect"] 
    anaerobic_effect = data["anaerobic_effect"]
    notes = data["notes"]
    
    with conn.session as session:
        session.execute(text("""
        INSERT INTO Cardio(date, time, name, distance, minutes, seconds, hr_avg, hr_max, pace, vo2_max, anaerobic_time, aerobic_time, intensive_time, light_time, aerobic_effect, anaerobic_effect, notes)
        VALUES(:date, :time, :name, :distance, :minutes, :seconds, :hr_avg, :hr_max, :pace, :vo2_max, :anaerobic_time, :aerobic_time, :intensive_time, :light_time, :aerobic_effect, :anaerobic_effect, :notes)
                            """), 
        {"date": date, "time": time, "name": name, "distance": distance, 
        "minutes": minutes, "seconds": seconds, "hr_avg": hr_avg, 
        "hr_max": hr_max, "pace": pace, "vo2_max": vo2_max, 
        "anaerobic_time": anaerobic_time, "aerobic_time": aerobic_time, 
        "intensive_time": intensive_time, "light_time": light_time, 
        "aerobic_effect": aerobic_effect, "anaerobic_effect": anaerobic_effect, 
        "notes": notes})
        session.commit()

    st.success("Measurement submitted successfully!")

def get_cardio_data() -> list:
    query = """
            SELECT date, name, distance, minutes, seconds, hr_avg, hr_max, vo2_max, pace, anaerobic_time, aerobic_time, intensive_time, light_time, aerobic_effect, anaerobic_effect
            FROM Cardio ORDER BY date DESC, time DESC
            """
    conn = get_conn()
    with conn.session as session:
        data = session.execute(text(query)).fetchall()
    return data

def insert_measurements(data: dict):
    conn = get_conn()

    date = data["date"]
    time = data["time"]
    weight = data["weight"]
    body_fat = data["body_fat"]
    waist = data["waist"]
    chest = data["chest"]
    shoulders = data["shoulders"]
    arms = data["arms"]
    thighs = data["thighs"]

    with conn.session as session:
        session.execute(text("""
            INSERT INTO Measurements(date, time, weight, body_fat, waist, chest, shoulders, arms, thighs)
            VALUES(:date, :time, :weight, :body_fat, :waist, :chest, :shoulders, :arms, :thighs)
            """), {"date": date, "time": time, "weight": weight, "body_fat": body_fat, "waist": waist, "chest": chest,
                    "shoulders": shoulders, "arms": arms, 
                    "thighs": thighs})
        session.commit()
        st.success("Measurements submitted successfully!")

def get_measurements_data() -> list:
    query = """
            SELECT date, waist, chest, shoulders, arms, thighs, weight, body_fat 
            FROM Measurements ORDER BY date
            """
    conn = get_conn()
    with conn.session as session:
        data = session.execute(text(query)).fetchall()
    return data

def insert_lifting(data: dict):
    conn = get_conn()

    date = data["date"]
    time = data["time"]
    area = data["area"]
    exercise = data["exercise"]
    set_number = data["set_number"]
    reps = data["reps"]
    weight = data["weight"]
    volume = data["volume"]
    rm = data["rm"]
    intensity = data["intensity"]
    notes = data["notes"]
    with conn.session as session:
        session.execute(text("""
            INSERT INTO Lifting(date, time, area, exercise, set_number, reps, weight, volume, rm, intensity, notes)
            VALUES(:date, :time, :area, :exercise, :set_number, :reps, :weight, :volume, :rm, :intensity, :notes)
            """), {"date": date, "time": time, "area": area, "exercise": exercise, "set_number": set_number, "reps": reps,
                    "weight": weight, "volume": volume, "rm": rm, "intensity": intensity, "notes": notes})
        session.commit()
        st.success("Exercise submitted successfully!")

def get_bodyweight_reps(exercise: str) -> list:
    reps_query = """
                SELECT date, MAX(reps) AS reps FROM Lifting
                WHERE exercise == :exercise
                GROUP BY date"""
    
    conn = get_conn()
    
    with conn.session as session:
        data = session.execute(text(reps_query), {"exercise": exercise}).fetchall()
    return data

def get_lifting_rm(exercise: str) -> list:
    rm_query = """
                SELECT date, MAX(rm) AS rm FROM Lifting
                WHERE exercise == :exercise
                GROUP BY date
            """
    conn = get_conn()
    with conn.session as session:
        data = session.execute(text(rm_query), {"exercise": exercise}).fetchall()

    return data

def get_lifting_intensity(exercise: str) -> list:
    query_intensity = """
                        SELECT date, MAX(intensity) AS intensity FROM Lifting
                        WHERE exercise == :exercise
                        GROUP BY date
                    """
    conn = get_conn()
    with conn.session as session:
        data = session.execute(text(query_intensity), {"exercise": exercise}).fetchall()

    return data

def get_lifting_volume(exercise: str) -> list:
    query_volume = """
                    SELECT date, SUM(volume) AS volume FROM Lifting
                    WHERE exercise == :exercise
                    GROUP BY date
                    """
    conn = get_conn()
    with conn.session as session:
        data = session.execute(text(query_volume), {"exercise": exercise}).fetchall()

    return data

def get_performed_exercises() -> list:
    query = """
            SELECT DISTINCT exercise FROM Lifting
            """
    conn = get_conn()
    with conn.session as session:
        data = session.execute(text(query)).fetchall()
    return [d[0] for d in data]

def get_performed_areas() -> list:
    query = """
            SELECT DISTINCT area FROM Lifting
            """
    conn = get_conn()
    with conn.session as session:
        data = session.execute(text(query)).fetchall()
    return [d[0] for d in data]

def get_performed_exercises_by_area(area: str) -> list:
    query = """
            SELECT DISTINCT exercise FROM Lifting
            WHERE area == :area
            """
    conn = get_conn()
    with conn.session as session:
        data = session.execute(text(query), {"area": area}).fetchall()
    return [d[0] for d in data]