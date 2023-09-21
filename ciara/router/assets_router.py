import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.ciara_models import TestAsset
from controllers.validator import TestAssetCreate
from models.session import get_db


logger = logging.getLogger(__name__)


db_session = Annotated[Session, Depends(get_db)]

router = APIRouter(prefix="/assets",
                   tags=["Asset Manager"],
                   responses={404: {"description": "Not found."}})


@router.post("/")
def create_asset(asset: TestAssetCreate, db: Session = Depends(get_db)):
    db_asset = TestAsset(**asset.dict())
    db.add(db_asset)
    db.commit()
    db.refresh(db_asset)
    return db_asset

@router.get("/",)
def get_all_assets(db: Session = Depends(get_db)):
    assets = db.query(TestAsset).all()
    return assets

@router.get("/{asset_id}")
def get_asset(asset_id: int, db: Session = Depends(get_db)):
    db_asset = db.query(TestAsset).filter(TestAsset.id == asset_id).first()
    if db_asset is None:
        raise HTTPException(status_code=404, detail="Asset not found")
    return db_asset