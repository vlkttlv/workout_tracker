from fastapi import APIRouter, Depends, Query
from app.exceptions import IncorrectIDOfShelduledWorkout, IncorrectIDOfWorkoutPlan, InvalidWorkoutStatusValue
from app.shelduled_workouts.dao import ShelduledWorkoutDAO
from app.shelduled_workouts.schemas import AddShelduledWorkout, UpdateShelduleWorkout
from app.users.dependencies import get_current_user
from app.workouts.dao import WorkoutPlansDAO


router = APIRouter(prefix='/shelduled_workouts', tags=['Shelduled workouts'])

@router.post('/', status_code=201,
             summary='Creates a shelduled workout')
async def add_shelduled_workout(shelduled_workout: AddShelduledWorkout,
                                current_user = Depends(get_current_user)):
    """Создает запланированную тренировку
    
    Аргументы:

        shelduled_date: date - Дата, на которую запланирована тренировка

        shelduled_time: time - Время, на которое запланирована тренировка (Часы и минуты)
    """
    workout_plan = await WorkoutPlansDAO.find_by_id(
        workout_plan_id=shelduled_workout.workout_plan_id,
        user_id=current_user.id)
    if workout_plan == []:
        raise IncorrectIDOfWorkoutPlan
    await ShelduledWorkoutDAO.add(workout_plan_id=shelduled_workout.workout_plan_id,
                                  user_id=current_user.id,
                                  shelduled_date=shelduled_workout.shelduled_date,
                                  shelduled_time=shelduled_workout.shelduled_time,
                                  status='pending')


@router.get('/', summary="Returns the user's shelduled workouts")
async def get_shelduled_workouts(status: str,
                                 order_by_time: str = Query(description="""Сортировка по возрастанию: asc,
                                                             по убыванию: desc"""),
                                 current_user = Depends(get_current_user)):
    """Возвращает все запланированные тренировки пользователя"""
    res = await ShelduledWorkoutDAO.find_all(asc_or_desc=order_by_time, user_id=current_user.id, status=status)
    return res


@router.get('/{shelduled_workout_id}', summary="Returns the user's shelduled workout by ID")
async def get_shelduled_workout(shelduled_workout_id: int,
                                current_user = Depends(get_current_user)):
    """Возвращает запланированную тренировку пользователя по ID"""
    res = await ShelduledWorkoutDAO.find_one_or_none(user_id=current_user.id,
                                                    id=shelduled_workout_id)
    return res


@router.patch('/{shelduled_workout_id}', summary='Updates time of the shelduled workout')
async def update_scheduled_workout(shelduled_workout_id: int,
                                   shelduled_workout: UpdateShelduleWorkout,
                                   current_user = Depends(get_current_user)):
    """
    Обновляет время запланированной тренировки
    """
    res = await ShelduledWorkoutDAO.find_one_or_none(user_id=current_user.id,
                                                     id=shelduled_workout_id)
    if res == []:
        raise IncorrectIDOfShelduledWorkout
    if shelduled_workout.shelduled_date is not None:
        await ShelduledWorkoutDAO.update(id=shelduled_workout_id,
                                         shelduled_date=shelduled_workout.shelduled_date)
    if shelduled_workout.shelduled_time is not None:
        await ShelduledWorkoutDAO.update(id=shelduled_workout_id,
                                         shelduled_time=shelduled_workout.shelduled_time)


@router.patch('/{shelduled_workout_id}/status', summary='Updates status of the shelduled workout')
async def update_status(shelduled_workout_id: int,
                        status: str = Query(default='in progress',
                                            description='Статус тренировки, например: in progress, done, skip'),
                        current_user = Depends(get_current_user)):
    """
    Обновляет статус запланированной тренировки
    """
    res = await ShelduledWorkoutDAO.find_one_or_none(user_id=current_user.id,
                                                     id=shelduled_workout_id)
    if res == []:
        raise IncorrectIDOfShelduledWorkout
    if status in ['done', 'skip', 'in progress']:
        await ShelduledWorkoutDAO.update(id=shelduled_workout_id,
                                         status=status)
    else:
        raise InvalidWorkoutStatusValue