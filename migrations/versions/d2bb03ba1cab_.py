"""empty message

Revision ID: d2bb03ba1cab
Revises: 2872fc818e4c
Create Date: 2023-12-07 14:21:37.570792

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd2bb03ba1cab'
down_revision = '2872fc818e4c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
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
    sa.Column('likes', sa.Integer(), nullable=True),
    sa.Column('dislikes', sa.Integer(), nullable=True),
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
    op.drop_table('admin')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('admin',
    sa.Column('Adminid', sa.INTEGER(), nullable=False),
    sa.Column('FirstName', sa.VARCHAR(length=500), nullable=True),
    sa.Column('LastName', sa.VARCHAR(length=500), nullable=True),
    sa.Column('Email', sa.VARCHAR(length=500), nullable=True),
    sa.Column('UserName', sa.VARCHAR(length=500), nullable=True),
    sa.Column('Password', sa.VARCHAR(length=500), nullable=True),
    sa.PrimaryKeyConstraint('Adminid')
    )
    op.drop_table('order_detail')
    op.drop_table('user')
    op.drop_table('product')
    op.drop_table('orders')
    # ### end Alembic commands ###