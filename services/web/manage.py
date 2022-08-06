from flask.cli import FlaskGroup

from project import app, db, User

cli = FlaskGroup(app)


@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command("seed_db")
def seed_db():
    db.session.add(User(email="nickdenisov@protonmail.com"))
    db.session.commit()


class Users:
    id = ''
    name = ''
    email = ''
    password = ''
    active = ''
    organization_roles = ''


class Organization:
    id = ''
    name = ''


class OrganizationRole:
    user_id = ''
    user = ''
    organization_id = ''
    organization = ''


if __name__ == "__main__":
    cli()
