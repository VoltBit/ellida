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
from flask import current_app as app
from flask_socketio import emit
from markupsafe import escape

from .forms import SignupForm
from .nav import nav

import zmq
import json
import os
import sys
import time
import random
from threading import Thread

import eventlet
eventlet.monkey_patch()

# sys.path.append(os.path.dirname(__name__))
# sys.path.append('/home/adobre/Dropbox/')
sys.path.append('../../')
from settings import EllidaSettings
from sockets import socketio

local_dir = os.path.dirname(__file__)
test_suite_path = u'../database/test_suite/'
spec_database_path = u'../database/'

frontend = Blueprint('frontend', __name__)

target_machine = '1'

nav.register_element('frontend_top', Navbar(
    View('Ellida framework', '.index'),
    View('Home', '.index'),
    View('Providers', '.providers'),
    # View('Results', '.results'),
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


@frontend.route('/')
def index():
    return render_template('index.html')

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

    # context = zmq.Context()
    # engine_socket = context.socket(zmq.PAIR)
    # engine_socket.connect("tcp://" + EllidaSettings.ENGINE_ADDR + ":" +
    #                        str(EllidaSettings.UI_SOCKET))

    # packet = {}
    # packet['event'] = "req_exe"
    # packet['value'] = request.form.getlist('check')
    # engine_socket.send_json(json.dumps(packet))
    # return json.dumps({'status': "sent", 'msg': packet['value']})
    feedback_thread = Thread(target=comm_manager,
        args=(request.form.getlist('check'),))
    feedback_thread.start()
    return json.dumps({'status': "sent", 'msg': 'ok'})

@frontend.route('/_cancel_run', methods=['GET', 'POST'])
def cancel_run():
    print("Closing run dialog")
    return "ok"

@frontend.route('/results/', methods=['GET', 'POST'])
def results():
    pass

@socketio.on('connection')
def conn_handler(json):
    print('received json: ' + str(json))

def comm_manager(args):
    context = zmq.Context()
    engine_socket = context.socket(zmq.PAIR)

    engine_socket.connect("tcp://" + EllidaSettings.ENGINE_ADDR + ":" +
                           str(EllidaSettings.UI_SOCKET))

    feedback_port = __get_rand_port()
    feedback_socket = context.socket(zmq.PAIR)
    feedback_socket.bind("tcp://*:%s" % feedback_port)

    packet = {}
    packet['event'] = "req_exe"
    packet['value'] = args
    packet['addr'] = EllidaSettings.UI_ADDR
    packet['port'] = str(feedback_port)
    print("sending:", packet)
    engine_socket.send_json(json.dumps(packet))
    engine_socket.close()

    while True:
        # packet = json.loads(feedback_socket.recv_json())
        packet = feedback_socket.recv()
        print("Received:", packet)
        if packet == bytes('ELLIDA_EXIT','utf-8'):
            socketio.emit('exit_event', {'data': 'EXIT'})
            break
        # print(packet['data'])
        # print(packet)
        socketio.emit('log_event', {'data': packet.decode('utf-8')})
    feedback_socket.close()
    print("UI communication ended")

def __get_rand_port(start=30000, end=35000):
    return random.randrange(start, end)

