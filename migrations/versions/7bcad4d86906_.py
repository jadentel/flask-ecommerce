"""empty message

Revision ID: 7bcad4d86906
Revises: 
Create Date: 2023-12-05 18:22:31.070933

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7bcad4d86906'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('admin',
    sa.Column('Adminid', sa.Integer(), nullable=False),
    sa.Column('FirstName', sa.String(length=500), nullable=True),
    sa.Column('LastName', sa.String(length=500), nullable=True),
    sa.Column('Email', sa.String(length=500), nullable=True),
    sa.Column('UserName', sa.String(length=500), nullable=True),
    sa.Column('Password', sa.String(length=500), nullable=True),
    sa.PrimaryKeyConstraint('Adminid')
    )
    op.create_table('orders',
    sa.Column('Orderid', sa.Integer(), nullable=False),
    sa.Column('OrderNumber', sa.String(length=500), nullable=True),
    sa.Column('UserID', sa.String(length=500), nullable=True),
    sa.Column('Phone', sa.String(length=500), nullable=True),
    sa.Column('Address', sa.String(length=500), nullable=True),
    sa.Column('OrderDate', sa.String(length=500), nullable=True),
    sa.Column('Price', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('Orderid')
    )
    op.create_table('product',
    sa.Column('Productid', sa.Integer(), nullable=False),
    sa.Column('ProductName', sa.String(length=500), nullable=True),
    sa.Column('Code', sa.String(length=500), nullable=True),
    sa.Column('Image', sa.String(length=500), nullable=True),
    sa.Column('Price', sa.Float(), nullable=True),
    sa.Column('Description', sa.String(length=500), nullable=True),
    sa.Column('Stock', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('Productid')
    )
    op.create_table('user',
    sa.Column('Userid', sa.Integer(), nullable=False),
    sa.Column('FirstName', sa.String(length=500), nullable=True),
    sa.Column('LastName', sa.String(length=500), nullable=True),
    sa.Column('Email', sa.String(length=500), nullable=True),
    sa.Column('UserName', sa.String(length=500), nullable=True),
    sa.Column('Password', sa.String(length=500), nullable=True),
    sa.PrimaryKeyConstraint('Userid')
    )
    op.create_table('order_detail',
    sa.Column('OrderDetailID', sa.Integer(), nullable=False),
    sa.Column('Orderid', sa.Integer(), nullable=True),
    sa.Column('OrderNumber', sa.Integer(), nullable=True),
    sa.Column('Userid', sa.Integer(), nullable=True),
    sa.Column('Productid', sa.Integer(), nullable=True),
    sa.Column('ProductCode', sa.String(length=500), nullable=True),
    sa.Column('Quantity', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['Orderid'], ['orders.Orderid'], ),
    sa.ForeignKeyConstraint(['Productid'], ['product.Productid'], ),
    sa.ForeignKeyConstraint(['Userid'], ['user.Userid'], ),
    sa.PrimaryKeyConstraint('OrderDetailID')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('order_detail')
    op.drop_table('user')
    op.drop_table('product')
    op.drop_table('orders')
    op.drop_table('admin')
    # ### end Alembic commands ###
