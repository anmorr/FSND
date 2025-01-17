"""empty message

Revision ID: 5fce18e8a068
Revises: ea96dc5f58f8
Create Date: 2021-07-05 22:57:20.516491

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5fce18e8a068'
down_revision = 'ea96dc5f58f8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Venue', sa.Column('seeking_description', sa.String(length=120), nullable=True))
    op.add_column('Venue', sa.Column('looking_for_talent', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Venue', 'looking_for_talent')
    op.drop_column('Venue', 'seeking_description')
    # ### end Alembic commands ###
