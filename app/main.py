from fastapi import FastAPI
from app.users.router import router as users_router
from app.exercises.router import router as exec_router
from app.workouts.router import router as work_rout
from app.shelduled_workouts.router import router as shelduled_router
from app.reports.router import router as report_router

app = FastAPI(title="Workout Tracker")

app.include_router(users_router)
app.include_router(exec_router)
app.include_router(work_rout)
app.include_router(shelduled_router)
app.include_router(report_router)
