def compute_volume(reps, weight):
    return reps * weight

def compute_rm(weight, reps):
    return weight * (1 + (reps / 30))

def compute_intensity(weight, rm):
    return 100 * weight / (rm + 0.001)