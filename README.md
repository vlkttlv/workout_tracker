# Трекер Тренировок

Пример реализации проекта трекера-тренировок с сайта [roadmap.sh](https://roadmap.sh/projects/fitness-workout-tracker)

## Установка и запуск


1. Склонируйте репозиторий:
   ```bash
   git clone https://github.com/vlkttlv/workout_tracker.git
   ```
2. Перейдите в папку проекта:
   ```bash
   cd workout_tracker
   ```
3. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```
4. Настройте переменные окружения. Создайте файл `.env` в корне проекта и добавьте необходимые параметры.
   
5. Прогоните миграции alembic:
   ```bash
   alembic upgrade head
   ```
6. Запуск Fastapi
   ```bash
   uvicorn app.main:app --reload
   ```
