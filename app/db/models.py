from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint, text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.inspection import inspect

Base = declarative_base()
metadata = Base.metadata


class Serializer(object):

    def serialize(self):
        return {c: getattr(self, c) for c in inspect(self).attrs.keys()}

    @staticmethod
    def serialize_list(l):
        return [m.serialize() for m in l]


class Course(Base):
    __tablename__ = 'course'

    id = Column(Integer, primary_key=True, server_default=text(
        "nextval('course_id_seq'::regclass)"))
    git_id = Column(Integer, nullable=False, unique=True)
    git_path = Column(String(255), nullable=False, unique=True)
    classroom_id = Column(String(255), nullable=False, unique=True)


class Owner(Base):
    __tablename__ = 'owner'

    id = Column(Integer, primary_key=True, server_default=text(
        "nextval('owner_id_seq'::regclass)"))
    email = Column(String(255), nullable=False, unique=True)


class Question(Base, Serializer):
    __tablename__ = 'question'

    question_id = Column(Integer, primary_key=True, unique=True,
                         server_default=text("nextval('question_id'::regclass)"))
    question_txt = Column(Text, nullable=False)
    mark = Column(Integer, nullable=False)
    answer_txt = Column(Text)
    max_attempts = Column(Integer, nullable=False,
                          server_default=text("10000"))

    def serialize(self):
        result = Serializer.serialize(self)
        return result


class TaskQuestion(Base):
    __tablename__ = 'task_question'

    task_id = Column(Integer, nullable=False)
    question_id = Column(Integer, nullable=False)
    id = Column(Integer, primary_key=True, server_default=text(
        "nextval('task_question_id_seq'::regclass)"))


class Task(Base, Serializer):
    __tablename__ = 'task'
    __table_args__ = (
        UniqueConstraint('classroom_id', 'grader_id'),
    )

    id = Column(Integer, primary_key=True, server_default=text(
        "nextval('task_id_seq'::regclass)"))
    name = Column(String(255), nullable=False)
    classroom_id = Column(String(255), nullable=False, unique=True)
    grader_id = Column(String(255), nullable=False)
    mode = Column(String(255), nullable=False)
    start = Column(DateTime, nullable=False)
    deadline = Column(DateTime, nullable=False)
    attempts = Column(Integer, nullable=False, server_default=text("100"))
    solution_filename = Column(String(255), nullable=False)
    description = Column(String(1000), nullable=False)
    technology = Column(String(255), nullable=False)
    course_id = Column(ForeignKey(
        'course.id', ondelete='CASCADE'), nullable=False)

    course = relationship('Course')

    def serialize(self):
        result = Serializer.serialize(self)
        return result


class Student(Base):
    __tablename__ = 'student'
    id = Column(Integer, primary_key=True, server_default=text(
        "nextval('student_id_seq'::regclass)"))
    classroom_id = Column(String(255), nullable=False, unique=True)
    email = Column(String(255), nullable=False, unique=True)


class StudentQuestion(Base):
    __tablename__ = 'student_question'

    def __init__(self, id, email, qua):
        self.id = id
        self.student_email = email
        self.question_id = qua

    id = Column(Text, primary_key=True, unique=True)
    student_email = Column(Text, nullable=False)
    question_id = Column(Text, nullable=False)
    answered = Column(Boolean, nullable=False, server_default=text("false"))
    attempts = Column(Integer, nullable=False, server_default=text("0"))


class TaskOwner(Base):
    __tablename__ = 'task_owner'
    __table_args__ = (
        UniqueConstraint('task_id', 'owner_id'),
    )

    id = Column(Integer, primary_key=True, server_default=text(
        "nextval('task_owner_id_seq'::regclass)"))
    task_id = Column(Integer, nullable=False)
    owner_id = Column(Integer, nullable=False)


class TaskStudent(Base):
    __tablename__ = 'task_student'
    __table_args__ = (
        UniqueConstraint('task_id', 'student_id'),
    )

    id = Column(Integer, primary_key=True, server_default=text(
        "nextval('task_student_id_seq'::regclass)"))
    task_id = Column(Integer, nullable=False)
    student_id = Column(Integer, nullable=False)
    grade = Column(Integer, nullable=False, server_default=text("0"))
    attempts = Column(Integer, nullable=False)
