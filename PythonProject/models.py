from sqlalchemy import Column, Integer, String
from database import Base


class Employee(Base):
   __tablename__ = "employees"


   id = Column(Integer, primary_key=True, index=True)
   first_name = Column(String(100))
   last_name = Column(String(100))
   email = Column(String(100), unique=True)
   department = Column(String(100))
