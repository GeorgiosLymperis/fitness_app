import streamlit as st
from sqlalchemy import text

@st.cache_resource
def get_conn():
    conn = st.connection("fitness", type="sql")
    return conn

def init_db():
    conn = get_conn()

    with conn.session as session:
        session.execute(text("""
                CREATE TABLE IF NOT EXISTS Measurements(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                time TEXT NOT NULL,
                weight REAL NOT NULL,
                body_fat REAL NOT NULL,
                waist REAL NOT NULL,
                chest REAL NOT NULL,
                shoulders REAL NOT NULL,
                arms REAL NOT NULL,
                thighs REAL NOT NULL
                )
                     """))

        session.execute(text("""
                        CREATE TABLE IF NOT EXISTS Lifting(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        date TEXT NOT NULL,
                        time TEXT NOT NULL,
                        area TEXT NOT NULL,
                        exercise TEXT NOT NULL,
                        set_number INTEGER NOT NULL,
                        reps INTEGER NOT NULL,
                        weight REAL NOT NULL,
                        volume REAL NOT NULL,
                        rm REAL NOT NULL,
                        intensity REAL NOT NULL,
                        notes TEXT
                        )
                        """))

        session.execute(text("""
                        CREATE TABLE IF NOT EXISTS Cardio(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        date TEXT NOT NULL,
                        time TEXT NOT NULL,
                        name TEXT NOT NULL,
                        distance REAL NOT NULL,
                        minutes REAL NOT NULL,
                        seconds REAL NOT NULL,
                        hr_avg REAL NOT NULL,
                        hr_max REAL NOT NULL,
                        pace REAL NOT NULL,
                        vo2_max REAL NOT NULL,
                        anaerobic_time REAL NOT NULL,
                        aerobic_time REAL NOT NULL,
                        intensive_time REAL NOT NULL,
                        light_time REAL NOT NULL,
                        aerobic_effect REAL NOT NULL,
                        anaerobic_effect REAL NOT NULL,
                        notes TEXT
                        )
                        """))
        session.commit()