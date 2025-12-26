import streamlit as st
from core.db import get_conn
from core.repositories import insert_cardio, get_cardio_data
import pandas as pd
import plotly.graph_objects as go


goals_levels = {
    "Level": ["Novice", "Beginner", "Intermediate", "Advanced", "Elite"],
    "Running_5k": ['31:29', '26:19', '22:32', '19:44', '17:40']
}

conn = get_conn()

with st.container():
    with st.popover("Add measurement"):
        st.markdown("Enter your measurements below:")
        date = st.date_input("Date")
        date = date.strftime("%Y-%m-%d")
        time = st.time_input("Time")
        time = time.strftime("%H:%M:%S")
        name = st.text_input("Name")
        distance = st.number_input("Distance", min_value=0.0, value=0.0, step=0.1)
        minutes = st.number_input("Minutes", min_value=0.0, value=0.0, step=0.1)
        seconds = st.number_input("Seconds", min_value=0.0, value=0.0, step=0.1)
        hr_avg = st.number_input("HR Avg", min_value=0.0, value=0.0, step=0.1)
        hr_max = st.number_input("HR Max", min_value=0.0, value=0.0, step=0.1)
        vo2_max = st.number_input("VO2 Max", min_value=0.0, value=0.0, step=0.1)
        pace = (minutes + (seconds / 60)) / (distance + 0.001)
        anaerobic_time = st.number_input("Anaerobic Time", min_value=0.0, value=0.0, step=0.1)
        aerobic_time = st.number_input("Aerobic Time", min_value=0.0, value=0.0, step=0.1)
        intensive_time = st.number_input("Intensive Time", min_value=0.0, value=0.0, step=0.1)
        light_time = st.number_input("Light Time", min_value=0.0, value=0.0, step=0.1)
        aerobic_effect = st.number_input("Aerobic Effect", min_value=0.0, value=0.0, step=0.1)
        anaerobic_effect = st.number_input("Anaerobic Effect", min_value=0.0, value=0.0, step=0.1)

        notes = st.text_area("Notes")

        if st.button("Submit"):
            insert_cardio({
                "date": date,
                "time": time,
                "name": name,
                "distance": distance,
                "minutes": minutes,
                "seconds": seconds,
                "hr_avg": hr_avg,
                "hr_max": hr_max,
                "pace": pace,
                "vo2_max": vo2_max,
                "anaerobic_time": anaerobic_time,
                "aerobic_time": aerobic_time,
                "intensive_time": intensive_time,
                "light_time": light_time,
                "aerobic_effect": aerobic_effect,
                "anaerobic_effect": anaerobic_effect,
                "notes": notes
            })

with st.container():
    data = get_cardio_data()
    df = pd.DataFrame(data, columns=["date", "name", "distance", "minutes", "seconds", 
                                     "hr_avg", "hr_max", "vo2_max", "pace", "anaerobic_time", 
                                     "aerobic_time", "intensive_time", "light_time", 
                                     "aerobic_effect", "anaerobic_effect"])
    df["minutes"] = df["minutes"] + df["seconds"]/60
    df['data'] = pd.to_datetime(df['date'])
    df = df.set_index('data')

    options = {
         "minutes": "minutes",
         "distance": "distance",
         "pace": "pace",
         "hr_avg": "hr_avg",
         "hr_max": "hr_max",
         "vo2_max": "vo2_max",
         "anaerobic_time": "anaerobic_time",
         "aerobic_time": "aerobic_time",
         "intensive_time": "intensive_time",
         "light_time": "light_time",
         "aerobic_effect": "aerobic_effect",
         "anaerobic_effect": "anaerobic_effect"
    }
    cardio_exercises = df["name"].unique()
    selected_name = st.selectbox("Select cardio exercise", cardio_exercises)
    df = df[df["name"] == selected_name]
    selected_label = st.selectbox("Select measurement", list(options.keys()))
    measurement_column = options[selected_label]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
         x=df.index,
         y=df[measurement_column],
         mode="lines+markers",
         name="Your Progress",
         hovertemplate="Date: %{x}<br>" + f"{selected_label}: "+"%{y}<extra></extra>",
            line=dict(color='blue')
    ))

    fig.update_layout(
        title=f"{selected_label} Progress Over Time",
        xaxis_title="Date",
        yaxis_title=selected_label,
        hovermode="x unified",
        legend_title="Legend",
        height=500
    )

    st.plotly_chart(fig, use_container_width=True)
