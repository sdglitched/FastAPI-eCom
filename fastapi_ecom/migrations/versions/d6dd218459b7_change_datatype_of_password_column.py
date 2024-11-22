"""change datatype of password column

Revision ID: d6dd218459b7
Revises: 306d801996a6
Create Date: 2024-07-26 22:07:29.440283

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'd6dd218459b7'
down_revision: Union[str, None] = '306d801996a6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('businesses', 'password',
               existing_type=sa.VARCHAR(length=100),
               type_=sa.Text(),
               existing_nullable=False)
    op.alter_column('customers', 'password',
               existing_type=sa.VARCHAR(length=100),
               type_=sa.Text(),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('customers', 'password',
               existing_type=sa.Text(),
               type_=sa.VARCHAR(length=100),
               existing_nullable=False)
    op.alter_column('businesses', 'password',
               existing_type=sa.Text(),
               type_=sa.VARCHAR(length=100),
               existing_nullable=False)
    # ### end Alembic commands ###
