# Api-Gateway/security.py
from fastapi import HTTPException, Security, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt

# Secret key to sign the JWTs (In production, keep this safe in a .env file!)
SECRET_KEY = "your-super-secret-key-change-this"
ALGORITHM = "HS256"

security = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    """
    This function intercepts the 'Authorization: Bearer <token>' header.
    It checks if the token is valid before letting the user through.
    """
    token = credentials.credentials
    try:
        # Decode the token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        
        # Return the payload so the Gateway knows WHO is making the request
        return payload
        
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")