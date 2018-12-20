import click
from datetime import datetime
from flask import current_app, g
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy

sql = SQLAlchemy()

class User(sql.Model):
    id = sql.Column(sql.Integer, primary_key=True)
    username = sql.Column(sql.String(80), unique=True, nullable=False)
    password = sql.Column(sql.String(80), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


class Post(sql.Model):
    id = sql.Column(sql.Integer, primary_key=True)
    title = sql.Column(sql.String(80), nullable=False)
    body = sql.Column(sql.Text, nullable=False)
    created = sql.Column(sql.DateTime, nullable=False,
        default=datetime.utcnow)

    author_id = sql.Column(sql.Integer, sql.ForeignKey('user.id'),
        nullable=False)
    author = sql.relationship('User',
        backref=sql.backref('posts', lazy=True))

    def __repr__(self):
        return '<Post %r>' % self.title


def init_db():
    with current_app.app_context():
        sql.drop_all()
        sql.create_all()

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    sql.init_app(app)
    app.cli.add_command(init_db_command)

