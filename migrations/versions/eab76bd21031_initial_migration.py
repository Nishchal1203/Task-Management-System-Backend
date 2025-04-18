"""Initial migration

Revision ID: eab76bd21031
Revises: 
Create Date: 2025-04-02 19:40:21.024604

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eab76bd21031'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=80), nullable=False),
    sa.Column('password_hash', sa.String(length=128), nullable=False),
    sa.Column('role', sa.String(length=20), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('task_manager',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=200), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('status', sa.String(length=20), nullable=False),
    sa.Column('priority', sa.String(length=20), nullable=False),
    sa.Column('due_date', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('task_manager', schema=None) as batch_op:
        batch_op.create_index('idx_task_manager_status', ['status'], unique=False)
        batch_op.create_index('idx_task_manager_user', ['user_id'], unique=False)

    op.create_table('task_logger',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('task_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=200), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('status', sa.String(length=20), nullable=False),
    sa.Column('priority', sa.String(length=20), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('logged_date', sa.Date(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['task_id'], ['task_manager.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('task_logger', schema=None) as batch_op:
        batch_op.create_index('idx_task_logger_date', ['logged_date'], unique=False)
        batch_op.create_index('idx_task_logger_task', ['task_id'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('task_logger', schema=None) as batch_op:
        batch_op.drop_index('idx_task_logger_task')
        batch_op.drop_index('idx_task_logger_date')

    op.drop_table('task_logger')
    with op.batch_alter_table('task_manager', schema=None) as batch_op:
        batch_op.drop_index('idx_task_manager_user')
        batch_op.drop_index('idx_task_manager_status')

    op.drop_table('task_manager')
    op.drop_table('users')
    # ### end Alembic commands ###
