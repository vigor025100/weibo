"""empty message

Revision ID: 558652693486
Revises: f4a8169fec1d
Create Date: 2020-08-25 19:48:16.109565

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '558652693486'
down_revision = 'f4a8169fec1d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'user', ['username'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', type_='unique')
    # ### end Alembic commands ###
