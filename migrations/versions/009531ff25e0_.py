"""empty message

Revision ID: 009531ff25e0
Revises: 
Create Date: 2020-09-20 12:14:44.223623

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '009531ff25e0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('mentors',
    sa.Column('userid', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('address', sa.String(), nullable=False),
    sa.Column('city', sa.String(), nullable=False),
    sa.Column('state', sa.String(), nullable=False),
    sa.Column('qualification', sa.String(), nullable=False),
    sa.Column('add_qualification', sa.String(), nullable=False),
    sa.Column('is_volunteer', sa.Boolean(), nullable=True),
    sa.Column('price', sa.Integer(), nullable=True),
    sa.Column('avail_time', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('userid')
    )
    op.create_table('students',
    sa.Column('userid', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('grade', sa.Integer(), nullable=False),
    sa.Column('address', sa.String(), nullable=False),
    sa.Column('city', sa.String(), nullable=False),
    sa.Column('state', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('userid')
    )
    op.create_table('admin_messages',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('mentor_id', sa.String(), nullable=True),
    sa.Column('student_id', sa.String(), nullable=True),
    sa.Column('message', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['mentor_id'], ['mentors.userid'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['student_id'], ['students.userid'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('feedbacks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('rating', sa.Integer(), nullable=False),
    sa.Column('message', sa.String(), nullable=True),
    sa.Column('mentor_id', sa.String(), nullable=True),
    sa.Column('student_id', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['mentor_id'], ['mentors.userid'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['student_id'], ['students.userid'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('mentor_courses',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('grade', sa.Integer(), nullable=False),
    sa.Column('mentor_id', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['mentor_id'], ['mentors.userid'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('mentor_student_pairs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('mentorship_year', sa.String(), nullable=True),
    sa.Column('present_student', sa.Boolean(), nullable=False),
    sa.Column('mentor_id', sa.String(), nullable=True),
    sa.Column('student_id', sa.String(), nullable=True),
    sa.Column('course_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['course_id'], ['mentor_courses.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['mentor_id'], ['mentors.userid'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['student_id'], ['students.userid'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('reply_messages',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('mentor_id', sa.String(), nullable=True),
    sa.Column('student_id', sa.String(), nullable=True),
    sa.Column('course_id', sa.Integer(), nullable=True),
    sa.Column('message', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['course_id'], ['mentor_courses.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['mentor_id'], ['mentors.userid'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['student_id'], ['students.userid'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('request_messages',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('mentor_id', sa.String(), nullable=True),
    sa.Column('student_id', sa.String(), nullable=True),
    sa.Column('course_id', sa.Integer(), nullable=True),
    sa.Column('message', sa.String(), nullable=True),
    sa.Column('needs_volunteer', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['course_id'], ['mentor_courses.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['mentor_id'], ['mentors.userid'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['student_id'], ['students.userid'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('request_messages')
    op.drop_table('reply_messages')
    op.drop_table('mentor_student_pairs')
    op.drop_table('mentor_courses')
    op.drop_table('feedbacks')
    op.drop_table('admin_messages')
    op.drop_table('students')
    op.drop_table('mentors')
    # ### end Alembic commands ###
