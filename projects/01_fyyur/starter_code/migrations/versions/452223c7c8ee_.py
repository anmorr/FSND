"""empty message

Revision ID: 452223c7c8ee
Revises: d565f7331071
Create Date: 2021-07-06 22:54:32.394828

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '452223c7c8ee'
down_revision = 'd565f7331071'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Artist', sa.Column('website_link', sa.String(length=120), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Artist', 'website_link')
    # ### end Alembic commands ###
