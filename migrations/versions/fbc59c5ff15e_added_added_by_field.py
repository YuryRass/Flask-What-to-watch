"""added added_by field

Revision ID: fbc59c5ff15e
Revises: 
Create Date: 2024-01-01 18:19:35.710356

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fbc59c5ff15e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('opinion',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=128), nullable=False),
    sa.Column('text', sa.Text(), nullable=False),
    sa.Column('source', sa.String(length=256), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.Column('added_by', sa.String(length=64), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('text')
    )
    with op.batch_alter_table('opinion', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_opinion_timestamp'), ['timestamp'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('opinion', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_opinion_timestamp'))

    op.drop_table('opinion')
    # ### end Alembic commands ###