"""добавили признак публикации

Revision ID: 056b9b459a47
Revises: 
Create Date: 2021-03-13 16:37:07.410589

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '056b9b459a47'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('jobs', sa.Column('is_published', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('jobs', 'is_published')
    # ### end Alembic commands ###
