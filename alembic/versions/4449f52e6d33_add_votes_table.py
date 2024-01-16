"""renaming <id> into <user_id> inside users table + add votes table

Revision ID: 4449f52e6d33
Revises: bb4bf97893aa
Create Date: 2024-01-15 19:46:33.225389

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4449f52e6d33'
down_revision: Union[str, None] = 'bb4bf97893aa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # First, rename the 'id' column in 'users' table to 'user_id'
    op.alter_column('users', 'id', new_column_name='user_id')

    # Then, you can proceed with the rest of your operations
    op.create_table('votes',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'post_id')
    )
    op.add_column('posts', sa.Column('user_id', sa.Integer(), nullable=False))
    op.drop_constraint('post_users_fk', 'posts', type_='foreignkey')
    op.create_foreign_key(None, 'posts', 'users', ['user_id'], ['user_id'], ondelete='CASCADE')
    op.drop_column('posts', 'owner_id')
    op.add_column('users', sa.Column('phone_number', sa.String(), nullable=True))

def downgrade() -> None:
    # Reverse your operations in the opposite order
    op.drop_column('users', 'phone_number')
    op.create_foreign_key('post_users_fk', 'posts', 'users', ['owner_id'], ['user_id'], ondelete='CASCADE')
    op.add_column('posts', sa.Column('owner_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'posts', type_='foreignkey')
    op.drop_column('posts', 'user_id')
    op.drop_table('votes')

    # Finally, rename the 'user_id' column back to 'id' in 'users' table
    op.alter_column('users', 'user_id', new_column_name='id')

