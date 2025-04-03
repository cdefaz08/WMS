from sqlalchemy.orm import Session
from models import RestockClass, PutawayClass, PickClass
from schemas.locationClases import (
    RestockClass as RestockClassSchema,
    RestockClassCreate,
    RestockClassUpdate,
    PutawayClass as PutawayClassSchema,
    PutawayClassCreate,
    PutawayClassUpdate,
    PickClass as PickClassSchema,
    PickClassCreate,
    PickClassUpdate
)

# ========== RESTOCK ==========
def create_restock_class(db: Session, class_data: RestockClassCreate):
    existing = db.query(RestockClass).filter(RestockClass.class_name == class_data.class_name).first()
    if existing:
        return {"error": "Restock class name already exists."}

    new_class = RestockClass(**class_data.dict())
    db.add(new_class)
    db.commit()
    db.refresh(new_class)
    return new_class


def get_restock_classes(db: Session):
    return db.query(RestockClass).all()


def update_restock_class(db: Session, class_id: int, class_data: RestockClassUpdate):
    db_class = db.query(RestockClass).filter(RestockClass.id == class_id).first()
    if db_class:
        for key, value in class_data.dict(exclude_unset=True).items():
            setattr(db_class, key, value)
        db.commit()
        db.refresh(db_class)
    return db_class


def delete_restock_class(db: Session, class_id: int):
    db_class = db.query(RestockClass).filter(RestockClass.id == class_id).first()
    if db_class:
        db.delete(db_class)
        db.commit()
    return db_class


# ========== PUTAWAY ==========
def create_putaway_class(db: Session, class_data: PutawayClassCreate):
    existing = db.query(PutawayClass).filter(PutawayClass.class_name == class_data.class_name).first()
    if existing:
        return {"error": "Putaway class name already exists."}

    new_class = PutawayClass(**class_data.dict())
    db.add(new_class)
    db.commit()
    db.refresh(new_class)
    return new_class


def get_putaway_classes(db: Session):
    return db.query(PutawayClass).all()


def update_putaway_class(db: Session, class_id: int, class_data: PutawayClassUpdate):
    db_class = db.query(PutawayClass).filter(PutawayClass.id == class_id).first()
    if db_class:
        for key, value in class_data.dict(exclude_unset=True).items():
            setattr(db_class, key, value)
        db.commit()
        db.refresh(db_class)
    return db_class


def delete_putaway_class(db: Session, class_id: int):
    db_class = db.query(PutawayClass).filter(PutawayClass.id == class_id).first()
    if db_class:
        db.delete(db_class)
        db.commit()
    return db_class


# ========== PICK ==========
def create_pick_class(db: Session, class_data: PickClassCreate):
    existing = db.query(PickClass).filter(PickClass.class_name == class_data.class_name).first()
    if existing:
        return {"error": "Pick class name already exists."}

    new_class = PickClass(**class_data.dict())
    db.add(new_class)
    db.commit()
    db.refresh(new_class)
    return new_class


def get_pick_classes(db: Session):
    return db.query(PickClass).all()


def update_pick_class(db: Session, class_id: int, class_data: PickClassUpdate):
    db_class = db.query(PickClass).filter(PickClass.id == class_id).first()
    if db_class:
        for key, value in class_data.dict(exclude_unset=True).items():
            setattr(db_class, key, value)
        db.commit()
        db.refresh(db_class)
    return db_class


def delete_pick_class(db: Session, class_id: int):
    db_class = db.query(PickClass).filter(PickClass.id == class_id).first()
    if db_class:
        db.delete(db_class)
        db.commit()
    return db_class
