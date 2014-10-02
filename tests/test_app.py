
from simple_sqlalchemy.example_app import *
import simple_sqlalchemy.config as cfg


def test_create_app():
    app = create_app()
    assert app.__dict__.has_key('url_map')

def test_config_app():
    app = Flask(__name__)
    config_app(app, cfg)
    assert app.config.has_key('SQLALCHEMY_DATABASE_URI')
    assert app.config['SQLALCHEMY_DATABASE_URI'] =='sqlite:///example.db'