"""empty message

Revision ID: 3a760ea411cf
Revises: ac868dd96865
Create Date: 2020-07-11 09:02:57.634797

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3a760ea411cf'
down_revision = 'ac868dd96865'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('categories', sa.Column('image', sa.String(length=100), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('categories', 'image')
    # ### end Alembic commands ###