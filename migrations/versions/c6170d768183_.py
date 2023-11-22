"""empty message

Revision ID: c6170d768183
Revises: 7ca4ff31656c
Create Date: 2023-11-21 16:03:24.441803

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c6170d768183'
down_revision = '7ca4ff31656c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('filme_comentario',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('data_criacao', sa.DateTime(), nullable=True),
    sa.Column('comentario', sa.String(), nullable=True),
    sa.Column('id_filme', sa.Integer(), nullable=True),
    sa.Column('id_user', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['id_filme'], ['filmes.id'], ),
    sa.ForeignKeyConstraint(['id_user'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('filme_comentario')
    # ### end Alembic commands ###
