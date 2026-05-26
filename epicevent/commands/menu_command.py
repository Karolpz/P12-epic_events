import click
from epicevent.utils.token import get_token, delete_token, verify_token
from epicevent.services.auth_service import AuthService
from epicevent.commands.auth_command import auth_command

def show_menu():
    while True:
        click.echo("\n Bienvenue sur Epic Events")
        
        token = get_token()
        valid_user = verify_token(token)
            
        if not valid_user:
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