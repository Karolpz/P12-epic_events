import click
from utils.token import get_token, delete_token
from services.auth_service import AuthService
from commands.auth_command import auth_command

def show_menu():
    while True:
        click.echo("\n Bienvenue sur Epic Events")
        
        if not get_token():
            click.echo("1. Se connecter")
            click.echo("0. Quitter")
            
            choice = click.prompt("Choix")
            
            if choice == "1":
                auth_command()
            elif choice == "0":
                break
        else:
            click.echo("2. Gérer les collaborateurs")
            click.echo("3. Gérer les clients")
            click.echo("4. Gérer les contrats")
            click.echo("5. Gérer les événements")
            click.echo("0. Se déconnecter")
            
            choice = click.prompt("Choix")
            
            if choice == "0":
                delete_token()
                click.echo("Au revoir !")   
            elif choice == "2":
                pass  # faire la gestions des rôles