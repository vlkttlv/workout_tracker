"""empty message

Revision ID: 818d6081f2d1
Revises: 30c6ca011956
Create Date: 2025-01-21 20:00:09.836026

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '818d6081f2d1'
down_revision: Union[str, None] = '30c6ca011956'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###

    op.add_column('workout_exercises', sa.Column('user_id', sa.Integer(), nullable=True))
    op.execute("UPDATE workout_exercises SET user_id = 1 WHERE user_id IS NULL")
    op.alter_column('workout_exercises', 'user_id', nullable=False)
    op.create_foreign_key(None, 'workout_exercises', 'users', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'workout_exercises', type_='foreignkey')
    op.drop_column('workout_exercises', 'user_id')
    # ### end Alembic commands ###
