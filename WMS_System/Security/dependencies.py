from fastapi import Header, HTTPException,Depends
from fastapi.security import OAuth2PasswordBearer
from Security.auth import verify_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login/")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = verify_access_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return user