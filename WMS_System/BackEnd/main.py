from fastapi import FastAPI, HTTPException, Depends
from routers.RuleMaintance import groups
from Security.dependencies import get_current_user
from Security.auth import create_access_token
from datetime import timedelta
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Request
from pydantic import BaseModel
from database import database, metadata, engine
from models import users
from routers.ItemMaintance import a_contents, item_default_config, item_maintance
from routers.LocationMaintance import proximity
from routers.OrderMaintance import order_line_routes, order_routes, order_type
from routers.PO_Maintance import purchase_order_line_routes, purchase_order_routes
from routers.ReceiptMaintance import receipt, receipt_line
from routers.RetailMaintance import sales
from routers.RuleMaintance import class_routes, group_classes
from routers.SystemMaintance import document_form, label_form, vendors_routes
from utils import  verify_password
from routers.SystemMaintance.users import router as users_router
from routers.ItemMaintance.items import router as items_router
from routers.ItemMaintance.ItemClass import router as item_class_router
from routers.LocationMaintance.LocationTypes import router as locationType_router
from routers.LocationMaintance.Location import router as locations
from routers.RuleMaintance import (rules)

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
        content={"detail": exc.errors()}  # ✅ No intentes volver a leer el body
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

@app.post("/login/")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    query = users.select().where(users.c.username == form_data.username)
    db_user = await database.fetch_one(query)

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(form_data.password, db_user["password"]):
        raise HTTPException(status_code=400, detail="Incorrect password")

    access_token_expires = timedelta(minutes=480)
    access_token = create_access_token(
        data={
            "sub": str(db_user["id"]),
            "username": db_user["username"]
        },
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer", "username": db_user["username"]}


app.include_router(users_router, prefix="/Users", tags=["Users"], dependencies=[Depends(get_current_user)])
app.include_router(items_router, prefix="/items", tags=["Items"], dependencies=[Depends(get_current_user)])
app.include_router(item_class_router, prefix="/item-classes", tags=["Item Classes"], dependencies=[Depends(get_current_user)])
app.include_router(locationType_router, prefix="/location-types",tags=["Location Types"], dependencies=[Depends(get_current_user)])
app.include_router(locations,prefix="/locations", tags=["locations"], dependencies=[Depends(get_current_user)])
app.include_router(class_routes.router)
app.include_router(vendors_routes.router)
app.include_router(purchase_order_line_routes.router)
app.include_router(purchase_order_routes.router)
app.include_router(order_routes.router)
app.include_router(order_line_routes.router)
app.include_router(proximity.router)
app.include_router(order_type.router)
app.include_router(document_form.router)
app.include_router(label_form.router)
app.include_router(receipt.router)
app.include_router(receipt_line.router)
app.include_router(item_maintance.router)
app.include_router(item_default_config.router)
app.include_router(a_contents.router)
app.include_router(sales.router)
app.include_router(groups.router)
app.include_router(group_classes.router)
app.include_router(rules.router)