from sqlalchemy import select
from app.dao.base import BaseDAO
from app.workouts.models import WorkoutPlans
from app.exercises.models import WorkoutExercise
from app.db.database import async_session_maker


class WorkoutPlansDAO(BaseDAO):

    model = WorkoutPlans

    @classmethod
    async def find_all(cls, user_id: int):
        async with async_session_maker() as session:
            
            # SELECT wp.id as workout_plan_id, wp.user_id, wp.name, wp.description,
            #        ws.exercise_id, ws.reps, ws.sets, ws.weight
            # from workout_plans as wp join workout_exercises as ws
            # on wp.id = ws.workout_plan_id
            
            stmt = (select(WorkoutPlans.id,
                          WorkoutPlans.user_id,
                          WorkoutPlans.name,
                          WorkoutPlans.description,
                          WorkoutExercise.exercise_id,
                          WorkoutExercise.reps,
                          WorkoutExercise.sets,
                          WorkoutExercise.weight,
                          )
                          .join(
                                WorkoutExercise,
                                WorkoutPlans.id == WorkoutExercise.workout_plan_id,
                                )
                                .where(WorkoutPlans.user_id == user_id))
            results = await session.execute(stmt)
            # Обработка результата
            workout_plan_data = {}
            for row in results:
                if row.id not in workout_plan_data:
                    workout_plan_data[row.id] = {
                        "workout_plan_id": row.id,
                        "user_id": row.user_id,
                        "name": row.name,
                        "description": row.description,
                        "exercises": [],
                    }
                workout_plan_data[row.id]["exercises"].append(
                    {
                        "exercise_id": row.exercise_id,
                        "reps": row.reps,
                        "sets": row.sets,
                        "weight": row.weight
                    })
            return list(workout_plan_data.values())