import os
import jinja2
from flask import Flask, render_template, current_app
from .config import ConfigFactory

###

app = Flask(__name__)
app.secret_key = 'UPAEnVMa'
# Loading the config
config_factory = ConfigFactory()
app.iconfig = config_factory.get_config()

# More templates
my_loader = jinja2.ChoiceLoader([
	jinja2.FileSystemLoader(app.iconfig.get('content', 'templates_directory')),
    app.jinja_loader,
])
app.jinja_loader = my_loader

###

from . import blog_entry
app.register_blueprint(blog_entry.bp)

from . import blog_list
app.register_blueprint(blog_list.bp)

from . import rss
app.register_blueprint(rss.bp)

###

app.jinja_env.globals['current_app'] = current_app

###

@app.errorhandler(404)
def not_found(error):
	return render_template('404.html'), 404
