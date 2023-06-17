# this is to help you to migrate
from main import app,db # this is to from the main  app
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db',MigrateCommand)

if __name__ == '__main__':
    manager.run()