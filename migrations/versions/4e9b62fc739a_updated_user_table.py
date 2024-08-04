"""updated user table

Revision ID: 4e9b62fc739a
Revises: 6fcad3990914
Create Date: 2024-08-02 16:31:35.924753

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4e9b62fc739a'
down_revision = '6fcad3990914'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('password', sa.String(length=256), nullable=True))
    op.create_unique_constraint(None, 'user', ['password'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', type_='unique')
    op.drop_column('user', 'password')
    # ### end Alembic commands ###
