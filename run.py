# run.py

import os

from flask_script import Manager
from app import create_app
from flask_migrate import Migrate, MigrateCommand


config_name = os.getenv('FLASK_CONFIGURATION','development')
app = create_app(config_name)
manager = Manager(app)


if __name__ == '__main__':
    app.run()
