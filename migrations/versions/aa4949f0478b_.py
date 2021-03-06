"""empty message

Revision ID: aa4949f0478b
Revises: 6f349dcb65c9
Create Date: 2020-08-27 15:34:55.258435

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aa4949f0478b'
down_revision = '6f349dcb65c9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('comment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uid', sa.Integer(), nullable=False),
    sa.Column('wid', sa.Integer(), nullable=False),
    sa.Column('cid', sa.Integer(), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_comment_cid'), 'comment', ['cid'], unique=False)
    op.create_index(op.f('ix_comment_uid'), 'comment', ['uid'], unique=False)
    op.create_index(op.f('ix_comment_wid'), 'comment', ['wid'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_comment_wid'), table_name='comment')
    op.drop_index(op.f('ix_comment_uid'), table_name='comment')
    op.drop_index(op.f('ix_comment_cid'), table_name='comment')
    op.drop_table('comment')
    # ### end Alembic commands ###
