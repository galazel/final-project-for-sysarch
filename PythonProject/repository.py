from sqlalchemy.orm import Session
from sqlalchemy import or_

from models import Employee
from schemas import EmployeeCreate, EmployeePatch


def create_employee(db: Session, employee: EmployeeCreate):

    existing = db.query(Employee).filter(Employee.email == employee.email).first()

    if existing:
        return None

    new_emp = Employee(
        first_name=employee.first_name,
        last_name=employee.last_name,
        email=employee.email.lower(),
        department=employee.department
    )

    db.add(new_emp)
    db.commit()
    db.refresh(new_emp)

    return new_emp


def get_employees(db: Session, search=None, department=None):

    query = db.query(Employee)

    if department:
        query = query.filter(Employee.department == department)

    if search:
        query = query.filter(
            or_(
                Employee.first_name.ilike(f"%{search}%"),
                Employee.last_name.ilike(f"%{search}%"),
                Employee.email.ilike(f"%{search}%"),
                Employee.department.ilike(f"%{search}%")
            )
        )

    return query.all()


def get_employee(db: Session, employee_id: int):
    return db.query(Employee).filter(Employee.id == employee_id).first()


def update_employee(db: Session, employee_id: int, employee: EmployeeCreate):

    emp = get_employee(db, employee_id)

    if not emp:
        return None

    emp.first_name = employee.first_name
    emp.last_name = employee.last_name
    emp.email = employee.email.lower()
    emp.department = employee.department

    db.commit()
    db.refresh(emp)

    return emp


def patch_employee(db: Session, employee_id: int, employee: EmployeePatch):

    emp = get_employee(db, employee_id)

    if not emp:
        return None

    if employee.first_name is not None:
        emp.first_name = employee.first_name

    if employee.last_name is not None:
        emp.last_name = employee.last_name

    if employee.email is not None:
        emp.email = employee.email.lower()

    if employee.department is not None:
        emp.department = employee.department

    db.commit()
    db.refresh(emp)

    return emp


def delete_employee(db: Session, employee_id: int):

    emp = get_employee(db, employee_id)

    if not emp:
        return None

    db.delete(emp)
    db.commit()

    return emp