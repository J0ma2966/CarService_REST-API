from flask import Flask, g
from sqlalchemy.orm import sessionmaker, Session


class DbMiddleware:
    def __init__(self, app: Flask, session_maker: sessionmaker):
        self.app = app
        self.session_maker = session_maker

    def open(self):
        session = self.session_maker()
        g.session = session

    def close(self, *_args, **_kwargs):
        g.session.close()

    def register(self):
        self.app.before_request(self.open)
        self.app.teardown_appcontext(self.close)
