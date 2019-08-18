"""empty message

Revision ID: f54815bb263b
Revises: 239a2d8ac940
Create Date: 2019-08-18 15:11:21.036349

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f54815bb263b'
down_revision = '239a2d8ac940'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task', sa.Column('status', sa.String(length=30), nullable=True))
    op.drop_column('task', 'complete')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task', sa.Column('complete', sa.BOOLEAN(), nullable=True))
    op.drop_column('task', 'status')
    # ### end Alembic commands ###
