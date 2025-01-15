from pydantic import BaseModel


class Exercises(BaseModel):

    id: int
    name: str
    category: str
    muscle_group: str
