from sqlalchemy import String,Integer,ForeignKey,Column,DateTime
from sqlalchemy.orm import relationship
from database import Base

class Student(Base):
    __tablename__="student"
    id = Column(Integer,primary_key=True)
    name = Column(String)
    email=Column(String,unique=True)
    phone=Column(String)
    roll_no=Column(String,unique=True)
    dob=Column(DateTime)
    faculty=Column(String)
    year=Column(Integer)
    semester=Column(Integer)
    hashed_password=Column(String)
    attendance=relationship("Attendance" , back_populates="student")
    submission=relationship("Submission" , back_populates="student")
    score=relationship("Score" , back_populates="student")


class Teacher(Base):
    __tablename__="teacher"
    id = Column(Integer,primary_key=True)
    name = Column(String)
    email=Column(String,unique=True)
    phone=Column(String)
    department=Column(String)
    faculty=Column(String)
    qualification=Column(String)
    hashed_password=Column(String)
    subject=relationship("Subject" , back_populates="teacher")
    assignment=relationship("Assignment" , back_populates="teacher")
    

class Subject(Base):
    __tablename__="subject"
    id = Column(Integer,primary_key=True)
    name = Column(String)
    credit_hr=Column(Integer)
    faculty=Column(String)
    semester=Column(Integer)
    teacher_id = Column(Integer,ForeignKey("teacher.id"))
    teacher = relationship("Teacher", back_populates="subject")
    attendance=relationship("Attendance" , back_populates="subject")
    assignment=relationship("Assignment" , back_populates="subject")
    test=relationship("Test" , back_populates="subject")



class Attendance(Base):
    __tablename__="attendance"
    id = Column(Integer,primary_key=True)
    date= Column(DateTime)
    status=Column(String)
    student_id = Column(Integer,ForeignKey("student.id"))
    subject_id = Column(Integer,ForeignKey("subject.id"))
    subject=relationship("Subject" , back_populates="attendance")
    student=relationship("Student" , back_populates="attendance")
    

class Assignment(Base):
    __tablename__="assignment"
    id = Column(Integer,primary_key=True)
    title=Column(String)
    deadline= Column(DateTime)
    description=Column(String)
    teacher_id = Column(Integer,ForeignKey("teacher.id"))
    subject_id = Column(Integer,ForeignKey("subject.id"))
    teacher=relationship("Teacher" , back_populates="assignment")
    subject=relationship("Subject" , back_populates="assignment")
    submission=relationship("Submission" , back_populates="assignment")


class Submission(Base):
    __tablename__="submission"
    id = Column(Integer,primary_key=True)
    status=Column(String)
    file_path= Column(String)
    submitted_at=Column(DateTime)
    assignment_id = Column(Integer,ForeignKey("assignment.id"))
    student_id = Column(Integer,ForeignKey("student.id"))
    assignment=relationship("Assignment" , back_populates="submission")
    student=relationship("Student" , back_populates="submission")
    


class Test(Base):
    __tablename__="test"
    id = Column(Integer,primary_key=True)
    name=Column(String)
    full_mark= Column(Integer)
    pass_mark =Column(Integer)
    date=Column(DateTime)
    subject_id = Column(Integer,ForeignKey("subject.id"))
    subject=relationship("Subject" , back_populates="test")
    score=relationship("Score" , back_populates="test")

class Score(Base):
    __tablename__="score"
    id = Column(Integer,primary_key=True)
    marks= Column(Integer)
    status =Column(String)
    test_id = Column(Integer,ForeignKey("test.id"))
    student_id = Column(Integer,ForeignKey("student.id"))
    student=relationship("Student" , back_populates="score")
    test=relationship("Test" , back_populates="score")

class Admin(Base):
    __tablename__ = "admin"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    hashed_password = Column(String)





