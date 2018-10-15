from application.apps import create_app
from instance.config import app_config

config_name=app_config['development']
app = create_app(config_name)
# method to run the flask app
if __name__ == '__main__':
    app.run()