insert_exec = """
INSERT INTO exercises (name, category, muscle_group) VALUES

('Махи гантелями в стороны', 'Силовое', 'Плечи'),
('Жим гири вверх двумя руками', 'Силовое', 'Плечи'),
('Тяга гири в наклоне одной рукой', 'Силовое', 'Спина, Щирочайшие, Трапеция'),
('Тяга гири к подбородку', 'Силовое', 'Плечи'),
('Французский жим с гирей стоя', 'Силовое', 'Трицепс'),
('Сгибание на бицепс двух рук с гирей', 'Силовое', 'Бицепс'),
('Отжимания', 'Силовое', 'Грудь'),
('Подтягивания', 'Силовое', 'Спина'),
('Болгарские выпады', 'Силовое', 'Ягодицы, Квадрицепс'),
('Румынская тяга', 'Силовое', 'Ягодицы, Бицепс бедра'),
('Ягодичный мост', 'Силовое', 'Ягодицы'),
('Приседания сумо', 'Силовое', 'Ягодицы, Внутрення сторона бедер'),
"""

"""
SELECT wp.id as workout_plan_id, wp.user_id, wp.name, wp.description,
ws.exercise_id, ws.reps, ws.sets, ws.weight, ex.name
from workout_plans as wp join workout_exercises as ws
on wp.id = ws.workout_plan_id
join shelduled_workout as sw on sw.workout_plan_id = wp.id
join exercises as ex on ws.exercise_id = ex.id
where sw.status = 'completed'
"""
