from fastapi import FastAPI

from database import engine, Base
from routes.employee import router as employee_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Company Internal Employee Management System"
)

app.include_router(employee_router)

@app.get("/")
def home():
    return {
        "message": "Company Internal Employee Management System"
    }
