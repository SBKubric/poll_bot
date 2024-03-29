"""Added is_terminated

Revision ID: 0841cec4f927
Revises: 39be4a35f501
Create Date: 2023-12-14 07:09:52.506091

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0841cec4f927'
down_revision = '39be4a35f501'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('polls', sa.Column('is_terminated', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('polls', 'is_terminated')
    # ### end Alembic commands ###
