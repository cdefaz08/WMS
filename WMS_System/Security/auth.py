from datetime import datetime, timedelta
from jose import JWTError, jwt

# Llave secreta para firmar el token
SECRET_KEY = "supersecretkey"  # Cámbiala por una más segura
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 480

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print("🔐 Token payload:", payload)
        return payload
    except JWTError as e:
        print("❌ Token is invalid or expired:", str(e))
        return None