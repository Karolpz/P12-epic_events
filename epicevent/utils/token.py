import jwt
import os
from datetime import datetime, timedelta, timezone
from epicevent.models import Collaborator
from epicevent.models.base import Session

def generate_token(collaborator):
    secret_key = os.getenv("JWT_SECRET_KEY")
    acces_payload = {
        "collaborator": {
            "id": collaborator.id,
            "role": collaborator.role.value
        },
        "exp": datetime.now(timezone.utc) + timedelta(minutes=15)
    }
    refresh_payload = {
        "collaborator": {
            "id": collaborator.id,
            "role": collaborator.role.value
        },
        "exp": datetime.now(timezone.utc) + timedelta(days=7)
    }
    access_token = jwt.encode(acces_payload, secret_key, algorithm="HS256")
    refresh_token = jwt.encode(refresh_payload, secret_key, algorithm="HS256")
    with open(".token", "w") as f:
        f.write(access_token)
    with open(".refresh_token", "w") as f:
        f.write(refresh_token)
    return access_token

def refresh_token():
    secret_key = os.getenv("JWT_SECRET_KEY")
    if not os.path.exists(".refresh_token"):
        return None
    try:
        with open(".refresh_token", "r") as f:
            refresh_token = f.read()
            payload = jwt.decode(refresh_token, secret_key, algorithms=["HS256"])
        with Session() as session:
            collaborator = session.query(Collaborator).filter_by(id=payload["collaborator"]["id"]).first()
            if not collaborator:
                return None
            generate_token(collaborator)
            return payload["collaborator"]
    except jwt.ExpiredSignatureError:
        delete_token()
        return None
    except jwt.InvalidTokenError:
        return None

def verify_token(token):
    secret_key = os.getenv("JWT_SECRET_KEY")
    try:
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        return payload["collaborator"]
    except jwt.ExpiredSignatureError:
        return refresh_token()
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
    if os.path.exists(".refresh_token"):
        os.remove(".refresh_token")
    return True

