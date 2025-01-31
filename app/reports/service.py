from datetime import date
import pandas as pd
from sqlalchemy import text
from app.db.database import async_session_maker


async def get_report_service(user_id: int, date_from: date, date_to: date):

    async with async_session_maker() as session:
        query = text("SELECT * FROM shelduled_workout")
        result = await session.execute(query)

    df = pd.DataFrame(result.fetchall(), columns=result.keys())
    df = (
        df[(df.shelduled_date >= date_from) & (df.shelduled_date <= date_to)]
        .groupby(["user_id", "status"])
        .agg({"status": "count"})
    )

    statuses = {}
    statuses_tuple = [
        (user_id, "completed"),
        (user_id, "pending"),
        (user_id, "in_progress"),
        (user_id, "skip"),
    ]

    for status in statuses_tuple:
        if df.index.isin([status]).any():
            statuses[f"count_{status[1]}_status"] = int(df.loc[status].status)
        else:
            statuses[f"count_{status[1]}_status"] = 0

    return statuses


# async def get_hist(user_id: int, exercise: str):
#     async with async_session_maker() as session:
#         query = text(f"""SELECT wp.id as workout_plan_id, wp.user_id, wp.name, wp.description,
#                      ws.exercise_id, ws.reps, ws.sets, ws.weight, ex.name, sw.shelduled_date
#                      from workout_plans as wp join workout_exercises as ws
#                      on wp.id = ws.workout_plan_id
#                      join shelduled_workout as sw on sw.workout_plan_id = wp.id
#                      join exercises as ex on ws.exercise_id = ex.id
#                      where sw.status = 'completed' and wp.user_id = {user_id} and ex.name = '{exercise}'""")
#         result = await session.execute(query)

#     df = pd.DataFrame(result.fetchall(), columns=result.keys())
#     df = df[['shelduled_date', 'weight']]
#     #     # Построим гистограмму
#     # plt.figure(figsize=(8, 6))
#     # plt.hist(df['shelduled_date'], bins=5, alpha=0.7, color='blue', edgecolor='black')
#     # plt.title('Histogram of Values')
#     # plt.xlabel('dates')
#     # plt.ylabel('weights')

#     print(df)
#     plt.figure(figsize=(5, 5))
#     sns.histplot(data=df, x="shelduled_date", y='weight', bins=1)
#     plt.title('Гистограмма упражнений (название в разработке)')
#     plt.xlabel('даты')
#     plt.ylabel('веса')
#     plt.grid(True)


#         # Сохраним изображение в буфер
#     buf = io.BytesIO()
#     plt.savefig(buf, format='png')
#     buf.seek(0)
#     plt.close()  # Закрываем фигуру

#     return buf
