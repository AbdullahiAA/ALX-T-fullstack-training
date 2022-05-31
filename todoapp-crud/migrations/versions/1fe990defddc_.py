"""empty message

Revision ID: 1fe990defddc
Revises: 052c48b4030e
Create Date: 2022-05-31 22:02:26.683278

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1fe990defddc'
down_revision = '052c48b4030e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('todos', 'todolists_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('todos', 'todolists_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###
