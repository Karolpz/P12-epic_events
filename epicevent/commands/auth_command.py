import click
from epicevent.services.auth_service import AuthService
from epicevent.models.base import Session
from epicevent.utils.token import delete_token, get_token

# def auth_command():
#     click.echo("Authentification")
#     email = click.prompt("Email")
#     password = click.prompt("Mot de passe", hide_input=True)
    
#     with Session() as session:
#         auth_service = AuthService(session)
#         collaborator = auth_service.login(email, password)
        
#         if collaborator:
#             click.echo(click.style(f"Bienvenue {collaborator.name} !", fg="green"))
#         else:
#             click.echo(click.style("Email ou mot de passe incorrect.", fg="red"))
    
#     return collaborator

@click.command()
def login():
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

@click.command()
def logout():
    delete_token()
    click.echo(click.style("Déconnexion réussie.", fg="green"))