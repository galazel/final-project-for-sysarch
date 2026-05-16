from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import Optional

from database import SessionLocal
import repository, schemas

router = APIRouter(prefix="/employees", tags=["Employees"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=schemas.EmployeeResponse)
def create_employee(employee: schemas.EmployeeCreate, db: Session = Depends(get_db)):

    try:
        result = repository.create_employee(db, employee)

        if result is None:
            raise HTTPException(status_code=400, detail="Email already exists")

        return result

    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email already exists")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=list[schemas.EmployeeResponse])
def get_employees(
    db: Session = Depends(get_db),
    search: Optional[str] = Query(None),
    department: Optional[str] = Query(None)
):

    try:
        return repository.get_employees(db, search, department)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{employee_id}", response_model=schemas.EmployeeResponse)
def get_employee(employee_id: int, db: Session = Depends(get_db)):

    try:
        emp = repository.get_employee(db, employee_id)

        if not emp:
            raise HTTPException(status_code=404, detail="Employee not found")

        return emp

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{employee_id}", response_model=schemas.EmployeeResponse)
def update_employee(employee_id: int, employee: schemas.EmployeeCreate, db: Session = Depends(get_db)):

    try:
        updated = repository.update_employee(db, employee_id, employee)

        if not updated:
            raise HTTPException(status_code=404, detail="Employee not found")

        return updated

    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email already exists")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{employee_id}", response_model=schemas.EmployeeResponse)
def patch_employee(employee_id: int, employee: schemas.EmployeePatch, db: Session = Depends(get_db)):

    try:
        updated = repository.patch_employee(db, employee_id, employee)

        if not updated:
            raise HTTPException(status_code=404, detail="Employee not found")

        return updated

    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email already exists")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{employee_id}")
def delete_employee(employee_id: int, db: Session = Depends(get_db)):

    try:
        deleted = repository.delete_employee(db, employee_id)

        if not deleted:
            raise HTTPException(status_code=404, detail="Employee not found")

        return {"message": "Employee deleted successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))