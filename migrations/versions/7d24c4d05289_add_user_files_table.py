"""Add user_files table

Revision ID: 7d24c4d05289
Revises: 50caa1ef002d
Create Date: 2023-03-31 19:27:24.695707

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7d24c4d05289'
down_revision = '50caa1ef002d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_files',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('file_name', sa.String(length=128), nullable=False),
    sa.Column('file_content', sa.Text(), nullable=False),
    sa.Column('upload_date', sa.DateTime(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_files')
    # ### end Alembic commands ###
