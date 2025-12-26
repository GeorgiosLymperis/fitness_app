import pandas as pd

def pd_to_kg(pounds):
    return pounds * 0.453592

leg_weight_exercises = {
    "label": "legs",
    "back_squat": "https://strengthlevel.com/strength-standards/squat",
    "front_squat": "https://strengthlevel.com/strength-standards/front-squat",
    "dumbbell_squat": "https://strengthlevel.com/strength-standards/dumbbell-squat",
    "seated_leg_curl": "https://strengthlevel.com/strength-standards/seated-leg-curl",
    "leg_extension": "https://strengthlevel.com/strength-standards/leg-extension",
    "horizontal_leg_press": "https://strengthlevel.com/strength-standards/horizontal-leg-press",
    "barbell_lunge": "https://strengthlevel.com/strength-standards/barbell-lunge",
    "dumbbell_lunge": "https://strengthlevel.com/strength-standards/dumbbell-lunge",
    "bulgarian_split_squat": "https://strengthlevel.com/strength-standards/bulgarian-split-squat",
    "sumo_squat": "https://strengthlevel.com/strength-standards/sumo-squat",
    "hip_adduction": "https://strengthlevel.com/strength-standards/hip-adduction",
    "seated_calf_raise": "https://strengthlevel.com/strength-standards/seated-calf-raise",
    "hip_abduction": "https://strengthlevel.com/strength-standards/hip-abduction"
}

leg_bodyweight_exercises = {
    "label": "legs",
    "lunge": "https://strengthlevel.com/strength-standards/lunge",
    "reverse_lunge": "https://strengthlevel.com/strength-standards/reverse-lunge",
    "side_lunge": "https://strengthlevel.com/strength-standards/side-lunge",
    "bodyweight_squat": "https://strengthlevel.com/strength-standards/bodyweight-squat",
    "pistol_squat": "https://strengthlevel.com/strength-standards/pistol-squat",
    "single_leg_squat": "https://strengthlevel.com/strength-standards/single-leg-squat",
    "glute_bridge": "https://strengthlevel.com/strength-standards/glute-bridge"
}

shoulder_weight_exercises = {
    "label": "shoulders",
    "dumbbell_shoulder_press": "https://strengthlevel.com/strength-standards/dumbbell-shoulder-press",
    "military_press": "https://strengthlevel.com/strength-standards/military-press",
    "machine_shoulder_press": "https://strengthlevel.com/strength-standards/machine-shoulder-press",
    "dumbbell_front_raise": "https://strengthlevel.com/strength-standards/dumbbell-front-raise",
    "dumbbell_upright_row": "https://strengthlevel.com/strength-standards/dumbbell-upright-row",
    "dumbbell_lateral_raise": "https://strengthlevel.com/strength-standards/dumbbell-lateral-raise",
    "cable_lateral_raise": "https://strengthlevel.com/strength-standards/cable-lateral-raise",
    "face_pull": "https://strengthlevel.com/strength-standards/face-pull"
}

shoulder_bodyweight_exercises = {
    "label": "shoulders",
    "headstand_push_ups": "https://strengthlevel.com/strength-standards/headstand-push-ups",
    "pike_push_ups": "https://strengthlevel.com/strength-standards/pike-push-up"
}

back_weight_exercises = {
    "label": "back",
    "bent_over_row": "https://strengthlevel.com/strength-standards/bent-over-row",
    "lat_pulldown": "https://strengthlevel.com/strength-standards/lat-pulldown",
    "dumbbell_row": "https://strengthlevel.com/strength-standards/dumbbell-row",
    "seated_cable_row": "https://strengthlevel.com/strength-standards/seated-cable-row",
    "close_grip_lat_pulldown": "https://strengthlevel.com/strength-standards/close-grip-lat-pulldown",
    "reverse_grip_lat_pulldown": "https://strengthlevel.com/strength-standards/reverse-grip-lat-pulldown",
    "cable_reverse_fly": "https://strengthlevel.com/strength-standards/cable-reverse-fly"
}

back_bodyweight_exercises = {
    "label": "back",
    "pull_ups": "https://strengthlevel.com/strength-standards/pull-ups",
    "chin_ups": "https://strengthlevel.com/strength-standards/chin-ups"
}

chest_weight_exercises = {
    "label": "chest",
    "bench_press": "https://strengthlevel.com/strength-standards/bench-press",
    "incline_bench_press": "https://strengthlevel.com/strength-standards/incline-bench-press",
    "chest_press": "https://strengthlevel.com/strength-standards/chest-press",
    "machine_chest_fly": "https://strengthlevel.com/strength-standards/machine-chest-fly",
    "dumbbell_fly": "https://strengthlevel.com/strength-standards/dumbbell-fly",
    "incline_dumbbell_fly": "https://strengthlevel.com/strength-standards/incline-dumbbell-fly",
    "incline_dumbbell_press": "https://strengthlevel.com/strength-standards/incline-dumbbell-bench-press",
    "dumbbell-bench-press": "https://strengthlevel.com/strength-standards/dumbbell-bench-press"
}

chest_bodyweight_exercises = {
    "label": "chest",
    "push_ups": "https://strengthlevel.com/strength-standards/push-ups",
    "one_arm_push_ups": "https://strengthlevel.com/strength-standards/one-arm-push-ups",
    "diamond_push_ups": "https://strengthlevel.com/strength-standards/diamond-push-ups",
    "decline_push_up": "https://strengthlevel.com/strength-standards/decline-push-up",
    "close_grip_push_up": "https://strengthlevel.com/strength-standards/close-grip-push-up"
}

biceps_weight_exercises = {
    "label": "biceps",
    "dumbbell_curl": "https://strengthlevel.com/strength-standards/dumbbell-curl",
    "barbell_curl": "https://strengthlevel.com/strength-standards/barbell-curl",
    "hammer_curl": "https://strengthlevel.com/strength-standards/hammer-curl",
    "cable_bicep_curl": "https://strengthlevel.com/strength-standards/cable-bicep-curl",
    "incline_dumbbell_curl": "https://strengthlevel.com/strength-standards/incline-dumbbell-curl",
    "dumbbell_concentration_curl": "https://strengthlevel.com/strength-standards/dumbbell-concentration-curl"
}

triceps_weight_exercises = {
    "label": "triceps",
    "tricep_pushdown": "https://strengthlevel.com/strength-standards/tricep-pushdown",
    "dumbbell_tricep_extension": "https://strengthlevel.com/strength-standards/dumbbell-tricep-extension",
    "cable_overhead_tricep_extension": "https://strengthlevel.com/strength-standards/cable-overhead-tricep-extension",
    "dumbbell_tricep_kickback": "https://strengthlevel.com/strength-standards/dumbbell-tricep-kickback"
}

triceps_bodyweight_exercises = {
    "label": "triceps",
    "bench_dips": "https://strengthlevel.com/strength-standards/bench-dips"
}

core_bodyweight_exercises = {
    "label": "core",
    "crunches": "https://strengthlevel.com/strength-standards/crunches",
    "sit_ups": "https://strengthlevel.com/strength-standards/sit-ups",
    "russian_twist": "https://strengthlevel.com/strength-standards/russian-twist",
    "hanging_leg_raise": "https://strengthlevel.com/strength-standards/hanging-leg-raise"
}

forearm_weight_exercises = {
    "label": "forearms",
    "wrist_curl": "https://strengthlevel.com/strength-standards/wrist-curl",
    "dumbbell_reverse_curl": "https://strengthlevel.com/strength-standards/dumbbell-reverse-curl"
}

weight_exercises = [
    leg_weight_exercises,
    shoulder_weight_exercises,
    back_weight_exercises,
    chest_weight_exercises,
    biceps_weight_exercises,
    triceps_weight_exercises,
    forearm_weight_exercises
]

bodyweight_exercises = [
    leg_bodyweight_exercises,
    back_bodyweight_exercises,
    chest_bodyweight_exercises,
    triceps_bodyweight_exercises,
    core_bodyweight_exercises
]

def get_weight_standards(exercises, save=False):
    df = pd.DataFrame()
    for body_area in exercises:
        for exercise, url in body_area.items():
            if exercise == "label":
                continue
            standards_df = pd.read_html(url)[2]
            standards_df = standards_df.apply(pd_to_kg, axis=1)
            standards_df['Area'] = body_area['label']
            standards_df['Exercise'] = exercise
            df = pd.concat([df, standards_df])
    if save:
        df.to_csv("weight_standards.csv")
    return df

def get_bodyweight_standards(exercises, save=False):
    df = pd.DataFrame()
    for body_area in exercises:
        for exercise, url in body_area.items():
            if exercise == "label":
                continue
            if exercise == "pull_ups" or exercise == "chin_ups":
                standards_df = pd.read_html(url)[2]
            else:
                standards_df = pd.read_html(url)[1]
            standards_df['Area'] = body_area['label']
            standards_df['Exercise'] = exercise
            df = pd.concat([df, standards_df])

    df['BW'] = df['BW'].apply(pd_to_kg)

    if save:
        df.to_csv("bodyweight_standards.csv")
    return df

goals_levels = {
    "Level": ["Novice", "Beginner", "Intermediate", "Advanced", "Elite"],
    "Waist": [84, 81, 79, 76, 74],
    "Chest": [96, 100, 104, 108, 112],
    "Shoulders": [112, 116, 120, 124, 128],
    "Arms Flexed": [32, 34, 36, 38, 40],
    "Arms Unflexed": [30, 32, 34, 36, 38],
    "Thighs": [52, 55, 58, 61, 64],
    "Calves": [35, 36, 37, 38, 39],
    "Weight": [70, 73, 75, 77, 79],
    "Body Fat": [17, 15, 13, 11, 9]
}

if __name__ == "__main__":
    get_weight_standards(weight_exercises, save=True)
    # get_bodyweight_standards(bodyweight_exercises, save=True)
    # goals_df = pd.DataFrame(goals_levels)
    # goals_df.to_csv("goals.csv")