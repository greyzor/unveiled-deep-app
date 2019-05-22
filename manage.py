"""
"""
import os
from flask_script import Manager
from unveiled.app import create_app #, db

app = create_app()
app.app_context().push()

manager = Manager(app)

@manager.command
def run():
	""" """
    app.run()

if __name__ == '__main__':
    manager.run()