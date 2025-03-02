from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
from db_service import UserDatabaseService
from get_token_data import get_token_data
from dotenv import load_dotenv
import os, json
load_dotenv()
env=os.getenv("ENV")
router=APIRouter(prefix='/auth')

@router.post('/login')
async def login_user(request: Request, user_db_service: UserDatabaseService=Depends()):
    if env=='test':
        with open("./mock_user_data.json", "r") as f:
            logged_in_user=json.loads(f)
        return logged_in_user
    id_token = request.headers.get('Authorization')
    if not id_token:
        return JSONResponse({"message":"No token provided", "data": None}, status_code=401)
    id_token = id_token.split('Bearer ')[-1]
    user_data=get_token_data(id_token)
    logged_in_user=await user_db_service.login_user(user_data)
    return logged_in_user


    
    
    