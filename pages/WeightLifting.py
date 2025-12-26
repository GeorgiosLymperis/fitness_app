import streamlit as st
import pandas as pd
import numpy as np
from core.db import get_conn
from core.services import compute_volume, compute_rm, compute_intensity
from core.repositories import (
    insert_lifting, get_bodyweight_reps, get_lifting_rm,
    get_lifting_intensity, get_lifting_volume,
    get_performed_areas, get_performed_exercises_by_area
    )
import plotly.graph_objects as go

conn = get_conn()

weight_df = pd.read_csv("utils/data/weight_standards.csv")
weight_df = weight_df.drop(columns=['Unnamed: 0'])
weight_df[weight_df.select_dtypes(include=['float']).columns] = weight_df.select_dtypes(include=['float']).round()

bodyweight_df = pd.read_csv("utils/data/bodyweight_standards.csv")
bodyweight_df = bodyweight_df.drop(columns=["Unnamed: 0"])
bodyweight_df[bodyweight_df.select_dtypes(include=['float']).columns] = bodyweight_df.select_dtypes(include=['float']).round()
bodyweight_df['Beg.'] = bodyweight_df['Beg.'].str.replace('< 1', '1')

bodyweight_df['Beg.'] = bodyweight_df['Beg.'].astype('int')

df = pd.concat([weight_df, bodyweight_df], axis=0)
df['Exercise'] = df["Exercise"].str.replace("_", " ").str.title()
df['Area'] = df["Area"].str.title()
body_weight = df['BW'].unique()
areas = df['Area'].unique()

@st.cache_data
def find_bodyweight(weight):
    return body_weight[np.abs(body_weight - weight).argmin()]

user_body_weight = st.number_input("Enter your bodyweight", min_value=0.0, value=0.0, step=0.1)
user_body_weight = find_bodyweight(user_body_weight)

with st.container():
    with st.popover("Add exercise"):
        st.markdown("Enter your exercise below:")
        date = st.date_input("Date")
        date = date.strftime("%Y-%m-%d")
        time = st.time_input("Time")
        time = time.strftime("%H:%M:%S")
        area = st.selectbox("Area", areas, key='area')
        df_exercises = df[df['Area'] == area]
        exercise = st.selectbox("Exercise", df_exercises['Exercise'].unique(), key='exercise_sbm')
        set_number = st.number_input("Set", min_value=0, value=0, step=1)
        reps = st.number_input("Reps", min_value=0, value=0, step=1)
        weight = st.number_input("Weight", min_value=0.0, value=0.0, step=0.1)
        volume = compute_volume(reps, weight)
        rm = compute_rm(weight, reps)
        intensity = compute_intensity(weight, rm)
        notes = st.text_area("Notes")
        if st.button("Submit"):
            insert_lifting({
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
                "notes": notes
            })

with st.container():
    performed_areas = pd.DataFrame(get_performed_areas(), columns=["area"])
    area_plt = st.selectbox("Area", performed_areas, key="area_plt")
    performed_exercises = pd.DataFrame(get_performed_exercises_by_area(area_plt), columns=["exercise"])
    exercise = st.selectbox("Exercise", performed_exercises, key="exercise_plt")
    exercise_label = ' '.join(exercise.split('_')).title()

    if exercise in bodyweight_df['Exercise'].unique():
        reps = get_bodyweight_reps(exercise)
        reps_df = pd.DataFrame(reps, columns=["date", "reps"])
        reps_df['date'] = pd.to_datetime(reps_df['date'])
        reps_df = reps_df.set_index('date')

        reps_fig = go.Figure()
        reps_fig.add_trace(go.Scatter(
            x = reps_df.index,
            y = reps_df['reps'],
            mode="lines+markers",
            name="Your Progress for Reps",
            hovertemplate="Date: %{x}<br>" + "Reps: "+"%{y}<extra></extra>",
            line=dict(color='blue')
        ))

        reps_levels = df[(df['Exercise']==exercise) & (df['BW']==user_body_weight)]
        for level in ['Beg.', 'Nov.', 'Adv.', 'Elite']:
            reps_fig.add_trace(go.Scatter(
                x=[reps_df.index.min(), reps_df.index.max()],
                y=[float(reps_levels[level].values[0])] * 2,
                mode="lines",
                name=level,
                line=dict(dash="dash", width=1),
                hoverinfo="skip"))
            
        reps_fig.update_layout(
            title=f"{exercise_label} Reps Progress Over Time",
            xaxis_title="Date",
            yaxis_title="RM",
            hovermode="x unified",
            legend_title="Legend",
            height=500
        )

        st.plotly_chart(reps_fig, use_container_width=True)
    else:

        lifting_rm = get_lifting_rm(exercise)
        rm_df = pd.DataFrame(lifting_rm, columns=["date", "rm"])
        rm_df['date'] = pd.to_datetime(rm_df['date'])
        rm_df = rm_df.set_index('date')

        rm_fig = go.Figure()
        rm_fig.add_trace(go.Scatter(
            x = rm_df.index,
            y = rm_df['rm'],
            mode="lines+markers",
            name="Your Progress for 1RM",
            hovertemplate="Date: %{x}<br>" + "RM: "+"%{y}<extra></extra>",
            line=dict(color='blue')
        ))

        rm_levels = df[(df['Exercise']==exercise) & (df['BW']==user_body_weight)]
        for level in ['Beg.', 'Nov.', 'Adv.', 'Elite']:
            rm_fig.add_trace(go.Scatter(
                x=[rm_df.index.min(), rm_df.index.max()],
                y=[float(rm_levels[level].values[0])] * 2,
                mode="lines",
                name=level,
                line=dict(dash="dash", width=1),
                hoverinfo="skip"))
            
        rm_fig.update_layout(
            title=f"{exercise_label} 1RM Progress Over Time",
            xaxis_title="Date",
            yaxis_title="RM",
            hovermode="x unified",
            legend_title="Legend",
            height=500
        )
        
        st.plotly_chart(rm_fig, use_container_width=True)

        lifting_intensity = get_lifting_intensity(exercise)
        intensity_df = pd.DataFrame(lifting_intensity, columns=["date", "intensity"])
        intensity_df['date'] = pd.to_datetime(intensity_df['date'])
        intensity_df = intensity_df.set_index('date')

        intensity_fig = go.Figure()
        intensity_fig.add_trace(go.Scatter(
            x=intensity_df.index,
            y=intensity_df['intensity'],
            mode="lines+markers",
            name="Your Progress for Intensity",
            hovertemplate="Date: %{x}<br>" + "Intensity: "+"%{y}<extra></extra>",
            line=dict(color='blue')
        ))

        intensity_fig.update_layout(
            title=f"{exercise_label} Intensity Progress Over Time",
            xaxis_title="Date",
            yaxis_title="RM",
            hovermode="x unified",
            legend_title="Legend",
            height=500
        )

        st.plotly_chart(intensity_fig, use_container_width=True)

        lifting_volume = get_lifting_volume(exercise)
        volume_df = pd.DataFrame(lifting_volume, columns=["date", "volume"])
        volume_df['date'] = pd.to_datetime(volume_df['date'])
        volume_df = volume_df.set_index('date')

        volume_fig = go.Figure()
        volume_fig.add_trace(go.Scatter(
            x=volume_df.index,
            y=volume_df['volume'],
            mode="lines+markers",
            name="Your Progress for Volume",
            hovertemplate="Date: %{x}<br>" + "Volume: "+"%{y}<extra></extra>",
            line=dict(color='blue')
        ))

        volume_fig.update_layout(
            title=f"{exercise_label} Volume Progress Over Time",
            xaxis_title="Date",
            yaxis_title="RM",
            hovermode="x unified",
            legend_title="Legend",
            height=500
        )

        st.plotly_chart(volume_fig, use_container_width=True)


