from functools import wraps
import click
from epicevent.utils.token import get_token, verify_token

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = get_token()
        if not token or not verify_token(token):
            click.echo("Authentification requise. Veuillez vous connecter.")
            return
        return f(*args, **kwargs)
    return decorated_function