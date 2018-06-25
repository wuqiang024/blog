"""init

Revision ID: dc7a17d762bb
Revises: 
Create Date: 2018-06-22 16:52:39.722243

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dc7a17d762bb'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('articleTypeSettings',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('protected', sa.Boolean(), nullable=True),
    sa.Column('hide', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('menus',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('order', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('sources',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=64), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=False),
    sa.Column('password_hash', sa.String(length=128), nullable=False),
    sa.Column('comfirmed', sa.Boolean(), nullable=True),
    sa.Column('avatar_hash', sa.String(length=32), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_table('articleTypes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('introduction', sa.Text(), nullable=True),
    sa.Column('menu_id', sa.Integer(), nullable=True),
    sa.Column('setting_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['menu_id'], ['menus.id'], ),
    sa.ForeignKeyConstraint(['setting_id'], ['articleTypeSettings.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('articles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=64), nullable=True),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('summary', sa.Text(), nullable=True),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('update_time', sa.DateTime(), nullable=True),
    sa.Column('num_of_view', sa.Integer(), nullable=True),
    sa.Column('articleType_id', sa.Integer(), nullable=True),
    sa.Column('source_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['articleType_id'], ['articleTypes.id'], ),
    sa.ForeignKeyConstraint(['source_id'], ['sources.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('title')
    )
    op.create_index(op.f('ix_articles_create_time'), 'articles', ['create_time'], unique=False)
    op.create_index(op.f('ix_articles_update_time'), 'articles', ['update_time'], unique=False)
    op.create_table('comments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('author_name', sa.String(length=64), nullable=True),
    sa.Column('author_email', sa.String(length=64), nullable=True),
    sa.Column('article_id', sa.Integer(), nullable=True),
    sa.Column('disabled', sa.Boolean(), nullable=True),
    sa.Column('comment_type', sa.String(length=64), nullable=True),
    sa.Column('replyTo', sa.String(length=128), nullable=True),
    sa.ForeignKeyConstraint(['article_id'], ['articles.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('comments')
    op.drop_index(op.f('ix_articles_update_time'), table_name='articles')
    op.drop_index(op.f('ix_articles_create_time'), table_name='articles')
    op.drop_table('articles')
    op.drop_table('articleTypes')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    op.drop_table('sources')
    op.drop_table('menus')
    op.drop_table('articleTypeSettings')
    # ### end Alembic commands ###