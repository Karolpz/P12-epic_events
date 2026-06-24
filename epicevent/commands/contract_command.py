import click
from epicevent.models.base import Session
from epicevent.utils.decorators import login_required, roles_required
from epicevent.utils.token import get_token, verify_token
from epicevent.services.contracts_service import ContractsService
from epicevent.services.collaborators_service import CollaboratorsService


@click.group()
def contracts():
    pass


@contracts.command()
@login_required
@click.option("--unsigned", is_flag=True, default=False, help="Contrats non signés uniquement")
@click.option("--unpaid", is_flag=True, default=False, help="Contrats non entièrement payés uniquement")
def list(unsigned, unpaid):
    payload = verify_token(get_token())
    collaborator_role = payload["role"]

    if (unsigned or unpaid) and collaborator_role != "commercial":
        click.echo(click.style("Ces options sont réservées au commercial.", fg="red"))
        return

    with Session() as session:
        service = ContractsService(session)

        if unsigned:
            contract_list = service.list_unsigned_contracts()
        elif unpaid:
            contract_list = service.list_unpaid_contracts()
        else:
            contract_list = service.list_contracts()

        if not contract_list:
            click.echo(click.style("Aucun contrat trouvé.", fg="yellow"))
            return

        click.echo(click.style("Liste des contrats :", fg="green"))
        for contract in contract_list:
            click.echo(
                f"- Contrat n° : {contract.id}, "
                f"Client: {contract.client.email}, "
                f"Montant: {contract.amount}, "
                f"Restant: {contract.amount_to_pay}, "
                f"Commercial: {contract.client.collaborator.name}, "
                f"Signé: {'Oui' if contract.is_signed else 'Non'}"
            )

@contracts.command()
@login_required
@roles_required("gestion")
def add():
    valid_user = verify_token(get_token())
    collaborator_id = valid_user["id"]
    client_mail = click.prompt("Email du client", type=str)

    with Session() as session:
        service = ContractsService(session)
        client = service.clients_service.get_client_by_email(client_mail)
        if not client:
            click.echo(click.style("Client introuvable.", fg="red"))
            return

        amount = click.prompt("Montant du contrat", type=float)

        try:
            contract = service.add_contract(client_mail, collaborator_id, amount)
        except Exception as e:
            click.echo(click.style(str(e), fg="red"))
            return
        click.echo(click.style(f"Contrat n° {contract.id} ajouté.", fg="green"))


@contracts.command()
@login_required
@roles_required("gestion", "commercial")
def update():
    contract_id = click.prompt("N° du contrat", type=int)

    payload = verify_token(get_token())
    collaborator_id = payload["id"]

    with Session() as session:
        collaborator_service = CollaboratorsService(session)
        collaborator = collaborator_service.get_collaborator_by_id(collaborator_id)
        contract_service = ContractsService(session)
        contract = contract_service.get_contract_by_id(contract_id)
        if not contract or not contract.can_edit(collaborator):
            click.echo(click.style("Contrat non trouvé ou accès refusé.", fg="red"))
            return

        click.echo(f"Contrat actuel — Montant: {contract.amount}, Restant: {contract.amount_to_pay}, Payé: {contract.amount - contract.amount_to_pay}")
        click.echo("Laissez vide pour ne pas modifier")
        amount = click.prompt("Nouveau montant total", default="")
        amount_to_pay = click.prompt("Nouveau montant restant", default="")

        kwargs = {}
        if amount:
            kwargs["amount"] = float(amount)
        if amount_to_pay:
            kwargs["amount_to_pay"] = float(amount_to_pay)

        try:
            contract_service.update_contract(contract_id, **kwargs)
        except Exception as e:
            click.echo(click.style(str(e), fg="red"))
            return
        click.echo(click.style("Contrat mis à jour !", fg="green"))


@contracts.command()
@login_required
@roles_required("gestion")
def sign():
    
    contract_id = click.prompt("N° du contrat", type=int)
    with Session() as session:
        contract_service = ContractsService(session)
        try:
            contract = contract_service.sign_contract(contract_id)
        except Exception as e:
            click.echo(click.style(str(e), fg="red"))
            return
        if contract:
            click.echo(click.style(f"Contrat signé : {contract.id}", fg="green"))
        else:
            click.echo(click.style("Contrat non trouvé.", fg="red"))
