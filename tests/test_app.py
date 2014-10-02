
from .example_app import *

KEEBLER_ELF = "Mary"

def test_create_app():
    app = Flask(__name__)
    assert app.__dict__.has_key('url_map')

def test_config_app():
    app = Flask(__name__)
    config_app(app)

    assert app.config.has_key('KEEBLER_ELF')
