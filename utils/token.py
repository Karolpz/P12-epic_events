import jwt
import os
from datetime import datetime, timedelta

def generate_token(collaborator):
    secret_key = os.getenv("JWT_SECRET_KEY")
    payload = {
        "collaborator": {
            "id": collaborator.id,
            "role": collaborator.role.value
        },
        "exp": datetime.utcnow() + timedelta(days=1)
    }
    token = jwt.encode(payload, secret_key, algorithm="HS256")
    with open(".token", "w") as f:
        f.write(token)
    return token

def verify_token(token):
    secret_key = os.getenv("JWT_SECRET_KEY")
    try:
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        return payload["collaborator"]
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
    
def get_token():
    if os.path.exists(".token"):
        with open(".token", "r") as f:
            token = f.read()
            return token
    return None

def delete_token():
    if os.path.exists(".token"):
        os.remove(".token")
        return True
    return False

