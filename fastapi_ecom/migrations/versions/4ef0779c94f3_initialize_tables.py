"""initialize tables

Revision ID: 4ef0779c94f3
Revises: 
Create Date: 2024-07-26 20:43:36.122183

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4ef0779c94f3'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('businesses',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('email_address', sa.String(length=100), nullable=False),
    sa.Column('password', sa.String(length=50), nullable=False),
    sa.Column('business_name', sa.String(length=100), nullable=False),
    sa.Column('address_line_1', sa.Text(), nullable=False),
    sa.Column('address_line_2', sa.Text(), nullable=True),
    sa.Column('city', sa.Text(), nullable=False),
    sa.Column('state', sa.Text(), nullable=False),
    sa.Column('is_verified', sa.Boolean(), nullable=True),
    sa.Column('creation_date', sa.Date(), nullable=False),
    sa.Column('uuid', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('uuid')
    )
    op.create_index(op.f('ix_businesses_email_address'), 'businesses', ['email_address'], unique=True)
    op.create_index(op.f('ix_businesses_id'), 'businesses', ['id'], unique=False)
    op.create_table('customers',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('email_address', sa.String(length=100), nullable=False),
    sa.Column('password', sa.String(length=50), nullable=False),
    sa.Column('full_name', sa.String(length=100), nullable=False),
    sa.Column('address_line_1', sa.Text(), nullable=False),
    sa.Column('address_line_2', sa.Text(), nullable=True),
    sa.Column('city', sa.Text(), nullable=False),
    sa.Column('state', sa.Text(), nullable=False),
    sa.Column('is_verified', sa.Boolean(), nullable=True),
    sa.Column('creation_date', sa.Date(), nullable=False),
    sa.Column('uuid', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('uuid')
    )
    op.create_index(op.f('ix_customers_email_address'), 'customers', ['email_address'], unique=True)
    op.create_index(op.f('ix_customers_id'), 'customers', ['id'], unique=False)
    op.create_table('orders',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('order_id', sa.Text(), nullable=False),
    sa.Column('user_id', sa.Text(), nullable=False),
    sa.Column('order_date', sa.Date(), nullable=False),
    sa.Column('total_price', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['customers.uuid'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('order_id')
    )
    op.create_index(op.f('ix_orders_id'), 'orders', ['id'], unique=False)
    op.create_table('products',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('product_name', sa.String(length=100), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('category', sa.String(length=50), nullable=False),
    sa.Column('manufacturing_date', sa.Date(), nullable=False),
    sa.Column('expiry_date', sa.Date(), nullable=False),
    sa.Column('product_price', sa.Float(), nullable=False),
    sa.Column('business_id', sa.Text(), nullable=False),
    sa.Column('uuid', sa.Text(), nullable=False),
    sa.ForeignKeyConstraint(['business_id'], ['businesses.uuid'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('uuid')
    )
    op.create_index(op.f('ix_products_id'), 'products', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_products_id'), table_name='products')
    op.drop_table('products')
    op.drop_index(op.f('ix_orders_id'), table_name='orders')
    op.drop_table('orders')
    op.drop_index(op.f('ix_customers_id'), table_name='customers')
    op.drop_index(op.f('ix_customers_email_address'), table_name='customers')
    op.drop_table('customers')
    op.drop_index(op.f('ix_businesses_id'), table_name='businesses')
    op.drop_index(op.f('ix_businesses_email_address'), table_name='businesses')
    op.drop_table('businesses')
    # ### end Alembic commands ###