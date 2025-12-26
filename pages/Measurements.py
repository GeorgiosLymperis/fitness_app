import streamlit as st
from core.db import get_conn
from core.repositories import insert_measurements, get_measurements_data
import pandas as pd
import plotly.graph_objects as go

conn = get_conn()

goals_levels = {
    "Level": ["Novice", "Beginner", "Intermediate", "Advanced", "Elite"],
    "Waist": [84, 81, 79, 76, 74],
    "Chest": [96, 100, 104, 108, 112],
    "Shoulders": [112, 116, 120, 124, 128],
    "Arms": [32, 34, 36, 38, 40],
    "Thighs": [52, 55, 58, 61, 64],
    "Weight": [70, 73, 75, 77, 79],
    "Body Fat": [17, 15, 13, 11, 9]
}

with st.container():
    with st.popover("Add measurement"):
        st.markdown("Enter your measurements below:")
        date = st.date_input("Date")
        date = date.strftime("%Y-%m-%d")
        time = st.time_input("Time")
        time = time.strftime("%H:%M:%S")
        weight = st.number_input("Weight", min_value=0.0, value=0.0, step=0.1)
        body_fat = st.number_input("Body Fat", min_value=0.0, value=0.0, step=0.1)
        waist = st.number_input("Waist", min_value=0.0, value=0.0, step=0.1)
        chest = st.number_input("Chest", min_value=0.0, value=0.0, step=0.1)
        shoulders = st.number_input("Shoulders", min_value=0.0, value=0.0, step=0.1)
        arms = st.number_input("Arms Flexed", min_value=0.0, value=0.0, step=0.1)
        thighs = st.number_input("Thighs", min_value=0.0, value=0.0, step=0.1)
        if st.button("Submit"):
            insert_measurements({
                "date": date,
                "time": time,
                "weight": weight,
                "body_fat": body_fat,
                "waist": waist,
                "chest": chest,
                "shoulders": shoulders,
                "arms": arms,
                "thighs": thighs,
            })

# with st.container():
#     st.markdown("View your measurements:")
#     with conn.session as session:
#         result = session.execute(text("""
#             SELECT * FROM Measurements
#             ORDER BY date DESC"""))
#         print(result.fetchall())
#         columns = result.keys()
#         rows = result.fetchall()
#         df_raw = pd.DataFrame(rows, columns=columns)
#         st.dataframe(df_raw)

data = get_measurements_data()
st.dataframe(data)

with st.container():

    df = pd.DataFrame(data, columns=["date", "waist", "chest", "shoulders", 
                                     "arms", "thighs", 
                                     "weight", "body_fat"])
    df['date'] = pd.to_datetime(df['date'])
    df = df.set_index('date')

    options = {
        "Waist": "waist",
        "Chest": "chest",
        "Shoulders": "shoulders",
        "Arms": "arms",
        "Thighs": "thighs",
        "Weight": "weight",
        "Body Fat": "body_fat"
    }
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

    for idx, level in enumerate(goals_levels["Level"]):
        fig.add_trace(go.Scatter(
            x=[df.index.min(), df.index.max()],
            y=[goals_levels[selected_label][idx], goals_levels[selected_label][idx]],
            mode="lines",
            name=level,
            line=dict(dash="dash", width=1),
            hoverinfo="skip"
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

