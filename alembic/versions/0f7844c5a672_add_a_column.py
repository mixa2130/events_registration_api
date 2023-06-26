"""Add a column

Revision ID: 0f7844c5a672
Revises: ca5f0ae50152
Create Date: 2023-06-17 17:41:03.219410

"""
from alembic import op
import sqlalchemy as sa
import fastapi_users_db_sqlalchemy

# revision identifiers, used by Alembic.
revision = '0f7844c5a672'
down_revision = 'ca5f0ae50152'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(table_name='event', schema='events',
                  column=sa.Column('creator_id', fastapi_users_db_sqlalchemy.generics.GUID(), nullable=False))

    # with op.batch_alter_table(table_name="event", schema='events') as batch_op:
    #     batch_op.create_foreign_key('fk__event__creator_id__user', 'user', ['creator_id'], ['id'],
    #                                 referent_schema='events')

    op.create_foreign_key(
        'fk__event__creator_id__user',
        source_table='event',
        referent_table='user',
        source_schema='events',
        referent_schema='events',
        local_cols=['creator_id'],
        remote_cols=['id']
    )


def downgrade() -> None:
    pass
