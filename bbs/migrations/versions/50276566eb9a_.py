"""empty message

Revision ID: 50276566eb9a
Revises: 5e5d28ad0420
Create Date: 2020-02-19 17:00:31.668995

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '50276566eb9a'
down_revision = '5e5d28ad0420'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cms_user', sa.Column('_password', sa.String(length=100), nullable=False))
    op.drop_column('cms_user', 'password')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cms_user', sa.Column('password', mysql.VARCHAR(length=100), nullable=False))
    op.drop_column('cms_user', '_password')
    # ### end Alembic commands ###
