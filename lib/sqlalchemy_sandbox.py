from datetime import datetime

from sqlalchemy import (
    create_engine, desc,
    CheckConstraint, PrimaryKeyConstraint, UniqueConstraint,
    Index, Column, DateTime, Integer, String
)
from sqlalchemy.orm import declarative_base, sessionmaker  # <-- fixed import here

Base = declarative_base()

class Student(Base):
    __tablename__ = 'students'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='id_pk'),
        UniqueConstraint('email', name='unique_email'),
        CheckConstraint('grade BETWEEN 1 AND 12', name='grade_between_1_and_12'),
        Index('index_name', 'name'),  # <-- moved into __table_args__
    )

    id = Column(Integer)
    name = Column(String)
    email = Column(String(55))
    grade = Column(Integer)
    birthday = Column(DateTime)
    enrolled_date = Column(DateTime, default=datetime.now)  # <-- callable, no ()

    def __repr__(self):
        return f"Student {self.id}: {self.name}, Grade {self.grade}"


if __name__ == '__main__':
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    albert_einstein = Student(
        name="Albert Einstein",
        email="albert.einstein@zurich.edu",
        grade=6,
        birthday=datetime(year=1879, month=3, day=14),
    )

    alan_turing = Student(
        name="Alan Turing",
        email="alan.turing@sherborne.edu",
        grade=11,
        birthday=datetime(year=1912, month=6, day=23),
    )

    session.add_all([albert_einstein, alan_turing])  # <-- add_all preferred here
    session.commit()

students = [student for student in session.query(Student)]
print(students)