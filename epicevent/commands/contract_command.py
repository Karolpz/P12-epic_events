import click
from epicevent.models.base import Session
from epicevent.utils.decorators import login_required, roles_required
from epicevent.utils.token import get_token, verify_token
from epicevent.services.contracts_service import ContractsService

@click.group()
def contracts():
    pass

@contracts.command()
@login_required
def list():
    with Session() as session:
        service = ContractsService(session)
        contracts = service.list_contracts()
        if not contracts:
            click.echo(click.style("Aucun contrat trouvé.", fg="yellow"))
            return
        
        click.echo(click.style("Liste des contrats :", fg="green"))
        for contract in contracts:
            click.echo(f"- Contrat n° : {contract.id}, Mail du client: {contract.client.email}, Montant: {contract.amount}")


@contracts.command()
@login_required
@roles_required("gestion")
def add():
    client_mail = click.prompt("Email du client", type=str)
    valid_user = verify_token(get_token())
    collaborator_id = valid_user["id"]
    amount = click.prompt("Montant du contrat", type=float)
    
    with Session() as session:
        service = ContractsService(session)
        contract = service.add_contract(client_mail, collaborator_id, amount)
        click.echo(f"Contrat ajouté : {contract.id}")


@contracts.command()
@login_required
@roles_required("gestion", "commercial")
def update():
    contract_id = click.prompt("N° du contrat", type=int)
    
    click.echo("Laissez vide pour ne pas modifier")
    amount = click.prompt("Nouveau montant", default="")
    amount_to_pay = click.prompt("Montant restant", default="")

    kwargs = {}
    if amount: kwargs["amount"] = float(amount)
    if amount_to_pay: kwargs["amount_to_pay"] = float(amount_to_pay)

    with Session() as session:
        service = ContractsService(session)
        payload = verify_token(get_token())
        collaborator_id = payload["id"]
        contract = service.update_contract(contract_id, collaborator_id, **kwargs)
        if contract:
            click.echo(f"Contrat mis à jour : {contract.id}")
        else:
            click.echo("Contrat non trouvé")

@contracts.command()
@login_required
@roles_required("gestion")
def sign():
    contract_id = click.prompt("N° du contrat", type=int)               
    with Session() as session:
        service = ContractsService(session)
        contract = service.sign_contract(contract_id)
        if contract:
            click.echo(f"Contrat signé : {contract.id}")
        else:
            click.echo("Contrat non trouvé")

@contracts.command()
@login_required
def delete():
    contract_id = click.prompt("N° du contrat", type=int)
    with Session() as session:
        service = ContractsService(session)
        if service.delete_contract(contract_id):
            click.echo(f"Contrat supprimé : {contract_id}")
        else:
            click.echo("Contrat non trouvé")

