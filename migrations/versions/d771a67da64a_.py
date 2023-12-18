"""empty message

Revision ID: d771a67da64a
Revises: 4505e98c480c
Create Date: 2023-12-18 21:53:20.207105

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd771a67da64a'
down_revision = '4505e98c480c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('planet', schema=None) as batch_op:
        batch_op.alter_column('climate',
               existing_type=sa.INTEGER(),
               type_=sa.String(length=80),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('planet', schema=None) as batch_op:
        batch_op.alter_column('climate',
               existing_type=sa.String(length=80),
               type_=sa.INTEGER(),
               existing_nullable=False)

    # ### end Alembic commands ###