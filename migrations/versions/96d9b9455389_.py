"""empty message

Revision ID: 96d9b9455389
Revises: aa4949f0478b
Create Date: 2020-08-28 19:41:36.473425

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '96d9b9455389'
down_revision = 'aa4949f0478b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('thumb',
    sa.Column('uid', sa.Integer(), nullable=False),
    sa.Column('wid', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('uid', 'wid')
    )
    op.add_column('article', sa.Column('n_thumb', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('article', 'n_thumb')
    op.drop_table('thumb')
    # ### end Alembic commands ###
