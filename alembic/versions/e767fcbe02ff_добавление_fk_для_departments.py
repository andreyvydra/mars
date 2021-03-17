"""добавление fk для departments

Revision ID: e767fcbe02ff
Revises: 3fe97e7b073b
Create Date: 2021-03-17 16:34:20.196899

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e767fcbe02ff'
down_revision = '3fe97e7b073b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'departments', 'users', ['chief'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'departments', type_='foreignkey')
    # ### end Alembic commands ###
