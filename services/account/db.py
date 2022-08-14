from sqlalchemy import (
    MetaData, Table, Column, ForeignKey, Integer, String, DateTime

)

from account import db

metadata = MetaData()


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    roles = db.relationship('Role', secondary='user_roles')

    def __init__(self, email):
        self.email = email


async def init_db(app):
    pass


async def get_user_by_name(conn, username):
    pass


async def get_users(conn):
    pass


async def register_user(conn):
    pass

