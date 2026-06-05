from functools import wraps
import click
from epicevent.utils.token import get_token, verify_token

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = get_token()
        if not token or not verify_token(token):
            click.echo(click.style("Authentification requise. Veuillez vous connecter.", fg="red"))
            return
        return f(*args, **kwargs)
    return decorated_function

def roles_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            payload = verify_token(get_token())
            if payload.get("role") not in roles:
                click.echo(click.style("Accès refusé.", fg="red"))
                return
            return f(*args, **kwargs)
        return decorated_function
    return decorator