"""profile_image

Revision ID: 8a83f38a6e85
Revises: 6753facb223b
Create Date: 2025-04-15 13:15:20.930902

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8a83f38a6e85'
down_revision: Union[str, None] = '6753facb223b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('profile_img', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'profile_img')
    # ### end Alembic commands ###
