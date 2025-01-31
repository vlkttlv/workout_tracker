from datetime import date
from fastapi import APIRouter, Depends
from app.reports.service import get_report_service
from app.users.dependencies import get_current_user


router = APIRouter(prefix="/reports", tags=["Reports"])


@router.get("/", summary="Returns the user's report")
async def get_report(date_from: date, date_to: date, current_user=Depends(get_current_user)):
    """Создает и возвращает отчет о тренировках
    (количество запланированных, законченных, начатых и пропущенных тренировок)"""
    res = await get_report_service(current_user.id, date_from, date_to)
    return res
