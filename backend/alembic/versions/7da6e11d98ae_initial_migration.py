"""initial migration

Revision ID: 7da6e11d98ae
Revises: 
Create Date: 2025-04-26 01:42:50.180456

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7da6e11d98ae'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 创建用户表
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('username')
    )
    
    # 创建论文表
    op.create_table(
        'papers',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('abstract', sa.Text(), nullable=True),
        sa.Column('keywords', sa.String(), nullable=True),
        sa.Column('status', sa.String(), nullable=False),
        sa.Column('target_conference', sa.String(), nullable=True),
        sa.Column('author_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['author_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # 创建评论表
    op.create_table(
        'reviews',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('paper_id', sa.Integer(), nullable=False),
        sa.Column('reviewer', sa.String(), nullable=False),
        sa.Column('score', sa.Integer(), nullable=False),
        sa.Column('comments', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['paper_id'], ['papers.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # 创建论文分析表
    op.create_table(
        'paper_analyses',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('paper_id', sa.Integer(), nullable=False),
        sa.Column('keywords', sa.String(), nullable=True),
        sa.Column('main_contribution', sa.Text(), nullable=True),
        sa.Column('methodology', sa.Text(), nullable=True),
        sa.Column('results', sa.Text(), nullable=True),
        sa.Column('limitations', sa.Text(), nullable=True),
        sa.Column('future_work', sa.Text(), nullable=True),
        sa.Column('total_citations', sa.Integer(), nullable=False, default=0),
        sa.Column('citation_types', sa.JSON(), nullable=True),
        sa.Column('citation_sentences', sa.JSON(), nullable=True),
        sa.Column('quality_scores', sa.JSON(), nullable=True),
        sa.Column('innovations', sa.JSON(), nullable=True),
        sa.Column('experiments', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['paper_id'], ['papers.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # 创建索引
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_papers_id'), 'papers', ['id'], unique=False)
    op.create_index(op.f('ix_reviews_id'), 'reviews', ['id'], unique=False)
    op.create_index(op.f('ix_paper_analyses_id'), 'paper_analyses', ['id'], unique=False)


def downgrade() -> None:
    # 删除索引
    op.drop_index(op.f('ix_paper_analyses_id'), table_name='paper_analyses')
    op.drop_index(op.f('ix_reviews_id'), table_name='reviews')
    op.drop_index(op.f('ix_papers_id'), table_name='papers')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    
    # 删除表
    op.drop_table('paper_analyses')
    op.drop_table('reviews')
    op.drop_table('papers')
    op.drop_table('users')
