from fastapi import APIRouter, Depends, JSONResponse
from app.db.db_service import WatchlistDatabaseService
from app.schemas.watchlist_create_request_model import WatchlistCreateRequestModel
from app.utils.logger import logger
router=APIRouter(prefix='/watchlist')

@router.post('/create', status_code=201)
async def create_watchlist(request_body: WatchlistCreateRequestModel, watchlist_db_service: WatchlistDatabaseService=Depends()):
    try:
        watchlist = request_body.watchlist
        uid = request_body.uid
        watchlist_data = watchlist.model_dump(by_alias=True)
        await watchlist_db_service.create_watchlist_in_db(uid, watchlist_data)
        return {"message": "Successfully created watchlist"}
    except Exception as e:
        logger.error(f"Error creating watchlist: {str(e)}")
        return JSONResponse({"message": "Error creating watchlist", "data": None}, status_code=500)
    