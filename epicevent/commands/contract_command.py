import click
from epicevent.models.base import Session
from epicevent.utils.decorators import login_required, roles_required
from epicevent.utils.token import get_token, verify_token
from epicevent.services.contracts_service import ContractsService
from epicevent.models.collaborators import Collaborator
from epicevent.models.contracts import Contract


@click.group()
def contracts():
    pass


@contracts.command()
@login_required
def list():
    with Session() as session:
        service = ContractsService(session)
        contract_list = service.list_contracts()
        if not contract_list:
            click.echo(click.style("Aucun contrat trouvé.", fg="yellow"))
            return

        click.echo(click.style("Liste des contrats :", fg="green"))
        for contract in contract_list:
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
        if not contract:
            click.echo(click.style("Client introuvable.", fg="red"))
            return
        click.echo(click.style(f"Contrat ajouté : {contract.id}", fg="green"))


@contracts.command()
@login_required
@roles_required("gestion", "commercial")
def update():
    contract_id = click.prompt("N° du contrat", type=int)

    payload = verify_token(get_token())
    collaborator_id = payload["id"]

    with Session() as session:
        collaborator = session.get(Collaborator, collaborator_id)
        contract = session.get(Contract, contract_id)
        if not contract or not contract.can_edit(collaborator):
            click.echo(click.style("Contrat non trouvé ou accès refusé.", fg="red"))
            return

        click.echo("Laissez vide pour ne pas modifier")
        amount = click.prompt("Nouveau montant", default="")
        amount_to_pay = click.prompt("Montant restant", default="")

        kwargs = {}
        if amount: 
            kwargs["amount"] = float(amount)
        if amount_to_pay: 
            kwargs["amount_to_pay"] = float(amount_to_pay)

        service = ContractsService(session)
        service.update_contract(contract_id, **kwargs)
        click.echo(click.style("Contrat mis à jour !", fg="green"))


@contracts.command()
@login_required
@roles_required("gestion")
def sign():
    contract_id = click.prompt("N° du contrat", type=int)
    with Session() as session:
        service = ContractsService(session)
        try:
            contract = service.sign_contract(contract_id)
        except Exception as e:
            click.echo(click.style(str(e), fg="red"))
            return
        if contract:
            click.echo(click.style(f"Contrat signé : {contract.id}", fg="green"))
        else:
            click.echo(click.style("Contrat non trouvé.", fg="red"))
