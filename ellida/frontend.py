# This contains our frontend; since it is a bit messy to use the @app.route
# decorator style when using application factories, all of our routes are
# inside blueprints. This is the front-facing blueprint.
#
# You can find out more about blueprints at
# http://flask.pocoo.org/docs/blueprints/

from flask import Blueprint, render_template, flash, redirect, url_for
from flask_bootstrap import __version__ as FLASK_BOOTSTRAP_VERSION
from flask_nav.elements import Navbar, View, Subgroup, Link, Text, Separator
from flask import request
from markupsafe import escape

from .forms import SignupForm
from .nav import nav

import zmq
import json
import os
import sys
import time
from multiprocessing import Process

sys.path.append(os.path.dirname(__name__))
# sys.path.append('/home/adobre/Dropbox/')
sys.path.append('../../')
from settings import EllidaSettings
import ellida

local_dir = os.path.dirname(__file__)
test_suite_path = u'../database/test_suite/'
spec_database_path = u'../database/'

frontend = Blueprint('frontend', __name__)

feedback_proc = None

# We're adding a navbar as well through flask-navbar. In our example, the
# navbar has an usual amount of Link-Elements, more commonly you will have a
# lot more View instances.
nav.register_element('frontend_top', Navbar(
    View('Ellida framework', '.index'),
    View('Home', '.index'),
    View('Providers', '.providers'),
    View('Results', '.results'),
    View('Test suite', '.test_suite'),
    Subgroup(
        'Specifications',
        View('CGL', '.specs', spec='cgl'),
        View('AGL', '.specs', spec='agl'), ),
    Subgroup(
        'Docs',
        Link('Flask-Bootstrap', 'http://pythonhosted.org/Flask-Bootstrap'),
        Link('Flask-AppConfig', 'https://github.com/mbr/flask-appconfig'),
        Link('Flask-Debug', 'https://github.com/mbr/flask-debug'),
        Separator(),
        Text('Bootstrap'),
        Link('Getting started', 'http://getbootstrap.com/getting-started/'),
        Link('CSS', 'http://getbootstrap.com/css/'),
        Link('Components', 'http://getbootstrap.com/components/'),
        Link('Javascript', 'http://getbootstrap.com/javascript/'),
        Link('Customize', 'http://getbootstrap.com/customize/'), ),
    # View('Forms Example', '.example_form'),
    Text('Using Flask-Bootstrap {}'.format(FLASK_BOOTSTRAP_VERSION)), ))


# Our index-page just shows a quick explanation. Check out the template
# "templates/index.html" documentation for more details.
@frontend.route('/')
def index():
    return render_template('index.html')

# Shows a long signup form, demonstrating form rendering.
@frontend.route('/example-form/', methods=('GET', 'POST'))
def example_form():
    form = SignupForm()

    if form.validate_on_submit():
        # We don't have anything fancy in our application, so we are just
        # flashing a message when a user completes the form successfully.
        #
        # Note that the default flashed messages rendering allows HTML, so
        # we need to escape things if we input user values:
        flash('Hello, {}. You have successfully signed up'
              .format(escape(form.name.data)))

        # In a real application, you may wish to avoid this tedious redirect.
        return redirect(url_for('.index'))

    return render_template('signup.html', form=form)

@frontend.route('/providers/')
def providers():
    return render_template('providers.html', providers=EllidaSettings.prov_list, test=False)

def make_tree(path, parent=""):
    tree = dict(name=os.path.basename(path), children=[])
    try: lst = os.listdir(path)
    except OSError:
        pass
    else:
        tree['parent'] = parent
        for name in lst:
            fn = os.path.join(path, name)
            if os.path.isdir(fn):
                tree['children'].append(make_tree(fn, tree['parent'] + '/' + tree['name']))
            else:
                if not "__init__" in name:
                    tree['children'].append(dict(name=name))
    return tree

@frontend.route('/specs/')
def specs():
    spec = request.args.get('spec')
    path = os.path.join(local_dir, spec_database_path + spec)
    print("Path:", path, "from specs_agl")
    values = request.form.getlist('check')
    print("Values:", values)
    return render_template('dirtree.html', tree=make_tree(path), test=False)

@frontend.route('/test_suite/', methods=['GET', 'POST'])
def test_suite():
    path = os.path.join(local_dir, test_suite_path)
    return render_template('dirtree.html', tree=make_tree(path), test=True)

@frontend.route('/_send_tests', methods=['GET', 'POST'])
def send_tests():
    """ Function for sending the selection to the engine. """
    global feedback_proc
    packet = {}
    packet['event'] = "req_exe"
    packet['value'] = request.form.getlist('check')
    ellida.engine_socket.send_json(json.dumps(packet))
    # feedback_proc = Process(target=__log_receiver, args=(), daemon=True)
    # feedback_proc.start()
    # print("Started", feedback_proc.pid)
    return json.dumps({'status': "sent", 'msg': packet['value']})

@frontend.route('/_cancel_run', methods=['GET', 'POST'])
def cancel_run():
    global feedback_proc
    print("Closing run dialog")
    feedback_proc.terminate()
    return "ok"

@frontend.route('/results/', methods=['GET', 'POST'])
def results():
    pass

def __log_receiver():
    print("Waiting...")
    packet = ellida.engine_socket.recv_json()
    packet = json.loads(packet)
    print("Received from engine: ", packet)
    return json.dumps(packet)
