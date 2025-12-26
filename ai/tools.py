from typing import Any, Dict, List
from core.repositories import (
    get_measurements_data,
    get_lifting_rm,
    get_lifting_volume,
    get_cardio_data,
    get_bodyweight_reps,
    get_lifting_intensity,
    get_performed_exercises,
    get_performed_areas,
    get_performed_exercises_by_area
)
from ai.rag import FitnessRAG

class FitnessTools:
    def __init__(self, rag: FitnessRAG):
        self.rag = rag

    def get_latest_measurements(self) -> Dict[str, Any]:
        data = get_measurements_data()
        if not data:
            return {"error": "No measurements found"}
        
        last = data[-1]
        keys = [
            "date", "waist", "chest", "shoulders",
            "arms", "thighs", "weight", "body_fat"
        ]
        return dict(zip(keys, last))
    
    def get_exercise_rm(self, exercise: str) -> List[Dict[str, Any]]:
        rows = get_lifting_rm(exercise)
        return [{"date": row[0], "rm": row[1]} for row in rows]
    
    def get_exercise_volume(self, exercise: str) -> List[Dict[str, Any]]:
        rows = get_lifting_volume(exercise)
        return [{"date": row[0], "volume": row[1]} for row in rows]
    
    def get_recent_cardio(self, limit: int = 5) -> List[Dict[str, Any]]:
        rows = get_cardio_data()
        recent = rows[:limit]
        keys = [
            "date", "name", "distance", "minutes",
            "seconds", "hr_avg", "hr_max", "vo2_max",
            "pace", "anaerobic_time", "aerobic_time",
            "intensive_time", "light_time",
            "aerobic_effect", "anaerobic_effect"
        ]
        return [dict(zip(keys, r)) for r in recent]

    def retrieve_knowledge(self, query: str, source: str | None = None, k: int = 3) -> List[str]:
        """
        Retrieves relevant knowledge from RAG.
        source: standards | rules
        """
        return self.rag.retrieve(query, k=k, source=source)
    
    def get_bodyweight_reps(self, exercise: str) -> List[Dict[str, Any]]:
        rows = get_bodyweight_reps(exercise)
        return [{"date": row[0], "reps": row[1]} for row in rows]
    
    def get_lifting_intensity(self, exercise: str) -> List[Dict[str, Any]]:
        rows = get_lifting_intensity(exercise)
        return [{"date": row[0], "intensity": row[1]} for row in rows]
    
    def get_performed_exercises(self) -> List[str]:
        return get_performed_exercises()
    
    def get_performed_areas(self) -> List[str]:
        return get_performed_areas()
    
    def get_performed_exercises_by_area(self, area: str) -> List[str]:
        return get_performed_exercises_by_area(area)
    