
from flask_simple_alchemy.examples.example_app import *
from flask_simple_alchemy.examples import config


def test_create_app():
    app = create_app()
    assert app.__dict__.has_key('url_map')

def test_config_app():
    app = Flask(__name__)
    config_app(app, config)
    assert app.config.has_key('SQLALCHEMY_DATABASE_URI')
    assert app.config.has_key('DEBUG')
    assert app.config.has_key('SECRET_KEY')
    assert app.config['SQLALCHEMY_DATABASE_URI'] =='sqlite:///example.db'
