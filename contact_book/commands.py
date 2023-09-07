import click
from models import Contact, session

@click.group()
def cli():
    pass

@cli.command()
@click.option('--name', prompt='Name', help='Contact name', required=True)
@click.option('--email', prompt='Email', help='Contact email')
@click.option('--phone', prompt='Phone', help='Contact phone')
def add(name, email, phone):
    contact = Contact(name=name, email=email, phone=phone)
    session.add(contact)
    session.commit()
    click.echo('Contact added successfully.')

@cli.command()
def view():
    contacts = session.query(Contact).all()
    if not contacts:
        click.echo('No contacts found.')
    else:
        for contact in contacts:
            click.echo(f'Name: {contact.name}, Email: {contact.email}, Phone: {contact.phone}')

@cli.command()
@click.option('--search', prompt='Search for a contact', help='Search contacts by name or email')
def search(search):
    contacts = session.query(Contact).filter(
        (Contact.name.contains(search)) | (Contact.email.contains(search))
    ).all()
    if not contacts:
        click.echo('No matching contacts found.')
    else:
        for contact in contacts:
            click.echo(f'Name: {contact.name}, Email: {contact.email}, Phone: {contact.phone}')

@cli.command()
@click.option('--name', prompt='Name of contact to update', help='Name of the contact to update')
@click.option('--new-name', prompt='New Name', help='New contact name')
@click.option('--new-email', prompt='New Email', help='New contact email')
@click.option('--new-phone', prompt='New Phone', help='New contact phone')
def update(name, new_name, new_email, new_phone):
    contact = session.query(Contact).filter_by(name=name).first()
    if contact:
        contact.name = new_name
        contact.email = new_email
        contact.phone = new_phone
        session.commit()
        click.echo(f'Contact "{name}" updated successfully.')
    else:
        click.echo(f'Contact "{name}" not found.')

@cli.command()
@click.option('--name', prompt='Name of contact to delete', help='Name of the contact to delete')
def delete(name):
    contact = session.query(Contact).filter_by(name=name).first()
    if contact:
        session.delete(contact)
        session.commit()
        click.echo(f'Contact "{name}" deleted successfully.')
    else:
        click.echo(f'Contact "{name}" not found.')

@cli.command()
@click.option('--sort', prompt='Sort contacts by name or email', help='Sort contacts by name or email')
def sort(sort):
    if sort == 'name':
        contacts = session.query(Contact).order_by(Contact.name).all()
    elif sort == 'email':
        contacts = session.query(Contact).order_by(Contact.email).all()
    else:
        click.echo('Invalid sorting option. Please choose "name" or "email".')
        return

    if not contacts:
        click.echo('No contacts found.')
    else:
        for contact in contacts:
            click.echo(f'Name: {contact.name}, Email: {contact.email}, Phone: {contact.phone}')

if __name__ == '__main__':
    cli()
