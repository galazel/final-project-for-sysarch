from fastapi import FastAPI


from database import engine, Base
from routes.employee import router as employee_router


Base.metadata.create_all(bind=engine)


app = FastAPI(
   title="Employee Management API"
)


app.include_router(employee_router)


@app.get("/")
def home():
   return {
       "message": "Employee Management System API"
   }