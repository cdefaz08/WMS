from fastapi import Header, HTTPException,Depends
from fastapi.security import OAuth2PasswordBearer
from Security.auth import verify_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login/")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = verify_access_token(token)

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user_id = payload.get("sub")
    username = payload.get("username")

    if not user_id or not username:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    return {
        "id": int(user_id),
        "username": username
    }

