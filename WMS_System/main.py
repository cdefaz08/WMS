from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi import Request
from pydantic import BaseModel
from database import database, metadata, engine
from models import users
from utils import  verify_password
from routers.users import router as users_router
from routers.items import router as items_router
from routers.ItemClass import router as item_class_router
from routers.LocationTypes import router as locationType_router
from routers.Location import router as locations

# Initialize FastAPI
app = FastAPI()

# Create database tables
metadata.create_all(engine)

class LoginRequest(BaseModel):
    username: str
    password: str

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "body": await request.json()},
    )

# Start & 
@app.on_event("startup")
async def startup():
    await database.connect()
#stop database connection
@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
#Get Root
@app.get("/")
async def read_root():
    return {"message": "Welcome to the FastAPI app!"}

#Validate Login
@app.post("/login/")
async def login(request: LoginRequest):
    query = users.select().where(users.c.username == request.username)
    db_user = await database.fetch_one(query)

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if not verify_password(request.password, db_user["password"]):
        raise HTTPException(status_code=400, detail="Incorrect password")
    
    return {"message": "Login successful!"}


app.include_router(users_router, prefix="/Users", tags=["Users"])
app.include_router(items_router, prefix="/items", tags=["Items"])
app.include_router(item_class_router, prefix="/item-classes", tags=["Item Classes"])
app.include_router(locationType_router, prefix="/location-types",tags=["Location Types"])
app.include_router(locations,prefix="/locations", tags=["locations"])
