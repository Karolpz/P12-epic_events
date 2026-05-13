import click
from services.auth_service import AuthService
from models.base import Session

def auth_command():
    click.echo("Authentification")
    email = click.prompt("Email")
    password = click.prompt("Mot de passe", hide_input=True)
    
    with Session() as session:
        auth_service = AuthService(session)
        collaborator = auth_service.login(email, password)
        
        if collaborator:
            click.echo(click.style(f"Bienvenue {collaborator.name} !", fg="green"))
        else:
            click.echo(click.style("Email ou mot de passe incorrect.", fg="red"))
    
    return collaborator