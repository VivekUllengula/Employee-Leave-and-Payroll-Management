from fastapi import FastAPI
from app.routes import employee, leave, payroll, user
from app.db.mongo import connect_to_db, close_mongo_connection
from app.core.config import settings

 
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION
    )

# Register routes
app.include_router(employee.router)
app.include_router(leave.router)
app.include_router(payroll.router)
app.include_router(user.router)

@app.on_event("startup")
async def startup_db_client():
    await connect_to_db()

@app.on_event("shutdown")
async def shutdown_db_client():
    await close_mongo_connection()
 
@app.get("/")
async def root():
    return {"message": "Employee Leave & Payroll Management System API is running"}

 