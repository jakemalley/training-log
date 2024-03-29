"""empty message

Revision ID: 24701eda5ed1
Revises: 43fa86f26e14
Create Date: 2015-02-03 16:45:32.166281

"""

# revision identifiers, used by Alembic.
revision = '24701eda5ed1'
down_revision = '43fa86f26e14'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Weight',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('weight', sa.Float(), nullable=False),
    sa.Column('member_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['member_id'], ['Member.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Weight')
    ### end Alembic commands ###
