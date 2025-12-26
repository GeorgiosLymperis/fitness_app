from typing import List, Dict, Any
from smolagents import tool, CodeAgent, InferenceClientModel
from ai.tools import FitnessTools

def fitness_agent(tools: FitnessTools) -> CodeAgent:
    @tool
    def get_latest_measurements() -> Dict[str, Any]:
        """
        Get the user's latest body measurements
        
        Returns:
            dict: dict with keys "date", "waist", "chest", "shoulders", "arms", "thighs", "weight", "body_fat"
        """
        return tools.get_latest_measurements()
    
    @tool
    def get_exercise_rm(exercise: str) -> List[Dict[str, Any]]:
        """
        Get max estimated repetition maximums (RM) per day for a given exercise.

        Args:
            exercise (str): The name of the exercise.

        Returns:
            list: A list of estimated RM values per day for the specified exercise.
                  For each day, the list contains a dictionary with keys "date" and "rm".
        """
        return tools.get_exercise_rm(exercise)
    
    @tool
    def get_exercise_volume(exercise: str) -> List[Dict[str, Any]]:
        """
        Get total training volume per day for an exercise.

        Args:
            exercise (str): The name of the exercise.

        Returns:
            list: A list of volume per day for the specified exercise.
                  For each day, the list contains a dictionary with keys "date" and "volume".
        """
        return tools.get_exercise_volume(exercise)
    
    @tool
    def get_recent_cardio(limit: int = 5) -> List[Dict[str, Any]]:
        """
        Get recent cardio sessions.

        Args:
            limit (int): The maximum number of recent cardio sessions to return.

        Returns:
            list: A list of recent cardio session records.
                  Each record is a dict with keys:
                  - "date": The date of the cardio session.
                  - "name": The name of the cardio activity.
                  - "distance": The distance covered in the cardio session in km.
                  - "minutes": The duration of the cardio session in minutes.
                  - "seconds": The duration of the cardio session in seconds.
                  - "hr_avg": The average heart rate during the cardio session.
                  - "hr_max": The maximum heart rate during the cardio session.
                  - "pace": The pace of the cardio session in minutes per km.
                  - "vo2_max": The maximum VO2 during the cardio session.
                  - "anaerobic_time": The anaerobic time during the cardio session in minutes.
                  - "aerobic_time": The aerobic time during the cardio session in minutes.
                  - "intensive_time": The intensive time during the cardio session in minutes.
                  - "light_time": The light time during the cardio session in minutes.
                  - "aerobic_effect": The aerobic effect during the cardio session.
                  - "anaerobic_effect": The anaerobic effect during the cardio session.
        """
        return tools.get_recent_cardio(limit)

    @tool
    def retrieve_knowledge(query: str, source: str = None, k: int = 3) -> List[str]:
        """
        Retrieve fitness knowledge from standards or rules.

        Args:
            query (str): The search query to match against the knowledge base.
            source (str, optional): The knowledge source to filter by (e.g., a standard or rule set).
            k (int): The number of results to return.

        Returns:
            list: A list of knowledge entries matching the query.
        """
        return tools.retrieve_knowledge(query, source, k)

    @tool
    def get_bodyweight_reps(exercise: str) -> List[Dict[str, Any]]:
        """
        Get repetitions for a bodyweight exercise.

        Args:
            exercise (str): The name of the bodyweight exercise.

        Returns:
            list: A list of repetitions per day for the specified exercise.
                  For each day, the list contains a dictionary with keys "date" and "reps".
        """
        return tools.get_bodyweight_reps(exercise)
    
    @tool
    def get_lifting_intensity(exercise: str) -> List[Dict[str, Any]]:
        """
        Get intensity levels for a lifting exercise.

        Args:
            exercise (str): The name of the lifting exercise.

        Returns:
            list: A list of intensity levels per day for the specified exercise.
                  For each day, the list contains a dictionary with keys "date" and "intensity".
        """
        return tools.get_lifting_intensity(exercise)
    
    @tool
    def get_performed_exercises() -> List[str]:
        """
        Get a list of exercises performed by the user.

        Returns:
            list: A list of exercise names.
        """
        return tools.get_performed_exercises()
    
    @tool
    def get_performed_areas() -> List[str]:
        """
        Get a list of exercised areas by the user.

        Returns:
            list: A list of area names.
        """
        return tools.get_performed_areas()
    
    @tool
    def get_performed_exercises_by_area(area: str) -> List[str]:
        """
        Get a list of exercises performed in a specific area.

        Args:
            area (str): The name of the area.

        Returns:
            list: A list of exercise names in the specified area.
        """
        return tools.get_performed_exercises_by_area(area)
    
    agent = CodeAgent(
        tools=[
            get_latest_measurements,
            get_exercise_rm,
            get_exercise_volume,
            get_recent_cardio,
            retrieve_knowledge,
            get_bodyweight_reps,
            get_lifting_intensity,
            get_performed_exercises,
            get_performed_areas,
            get_performed_exercises_by_area
        ],
        model=InferenceClientModel(),
    )

    return agent