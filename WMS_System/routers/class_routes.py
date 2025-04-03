from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from crud import class_crud
from schemas.locationClases import RestockClass, RestockClassCreate, RestockClassUpdate , PutawayClass , PutawayClassCreate , PutawayClassUpdate
from schemas.locationClases import PickClass , PickClassCreate , PickClassUpdate

router = APIRouter(prefix="/classes", tags=["Classes"])

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# RESTOCK ENDPOINTS
@router.post("/restock", response_model=RestockClass)
def create_restock_class(class_data: RestockClassCreate, db: Session = Depends(get_db)):
    return class_crud.create_restock_class(db, class_data)

@router.get("/restock", response_model=list[RestockClass])
def read_restock_classes(db: Session = Depends(get_db)):
    return class_crud.get_restock_classes(db)

@router.put("/restock/{class_id}", response_model=RestockClass)
def update_restock_class(class_id: int, class_data: RestockClassUpdate, db: Session = Depends(get_db)):
    return class_crud.update_restock_class(db, class_id, class_data)

@router.delete("/restock/{class_id}")
def delete_restock_class(class_id: int, db: Session = Depends(get_db)):
    return class_crud.delete_restock_class(db, class_id)


# Repeat the same for PUTAWAY and PICK
@router.post("/putaway", response_model=PutawayClass)
def create_putaway_class(class_data: PutawayClassCreate, db: Session = Depends(get_db)):
    return class_crud.create_putaway_class(db, class_data)

@router.get("/putaway", response_model=list[PutawayClass])
def read_putaway_classes(db: Session = Depends(get_db)):
    return class_crud.get_putaway_classes(db)

@router.put("/putaway/{class_id}", response_model=PutawayClass)
def update_putaway_class(class_id: int, class_data: PutawayClassUpdate, db: Session = Depends(get_db)):
    return class_crud.update_putaway_class(db, class_id, class_data)

@router.delete("/putaway/{class_id}")
def delete_putaway_class(class_id: int, db: Session = Depends(get_db)):
    return class_crud.delete_putaway_class(db, class_id)


@router.post("/pick", response_model=PickClass)
def create_pick_class(class_data: PickClassCreate, db: Session = Depends(get_db)):
    return class_crud.create_pick_class(db, class_data)

@router.get("/pick", response_model=list[PickClass])
def read_pick_classes(db: Session = Depends(get_db)):
    return class_crud.get_pick_classes(db)

@router.put("/pick/{class_id}", response_model=PickClass)
def update_pick_class(class_id: int, class_data: PickClassUpdate, db: Session = Depends(get_db)):
    return class_crud.update_pick_class(db, class_id, class_data)

@router.delete("/pick/{class_id}")
def delete_pick_class(class_id: int, db: Session = Depends(get_db)):
    return class_crud.delete_pick_class(db, class_id)
