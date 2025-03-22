from fastapi import APIRouter, Depends
from app.core.equity_database import EquityDatabase


def get_equity_database():
    return EquityDatabase(data_path="./app/assets/data/equities.csv")

router = APIRouter(prefix="/equities")

@router.get("/all")
def get_all_equity_data(equity_db: EquityDatabase = Depends(get_equity_database)):
    return equity_db.get_all_equities()

@router.get("/search")
def search_equities(ticker: str, equity_db: EquityDatabase = Depends(get_equity_database)):
    return equity_db.search_equities(ticker)

