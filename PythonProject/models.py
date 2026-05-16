from sqlalchemy import Column, Integer, String, DateTime, Numeric
from database import Base


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    department = Column(String(100), nullable=False)
    salary = Column(Numeric(precision=10, scale=2), nullable=False)
    hireDate = Column(DateTime, nullable=False)