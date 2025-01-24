from datetime import date, time
from pydantic import BaseModel, Field


class AddShelduledWorkout(BaseModel):
    workout_plan_id: int = Field()
    shelduled_date: date = Field(description='Дата, на которую запланирована тренировка')
    shelduled_time: time = Field(description='Время, на которое запланирована тренировка')

class ShelduledWorkout(BaseModel):
    id: int
    user_id: int
    workout_plan_id: int
    shelduled_date: date
    shelduled_time: time 
    status: str