#!/usr/bin/python3.5

import os
import sys
from sockets import socketio
from ellida import create_app

sys.path.append(os.path.dirname(__name__))

def main():
    # create an app instance
    app = create_app()

    # app.run(debug=True)
    # app.run(host='0.0.0.0')
    socketio.init_app(app)
    socketio.run(app, host='0.0.0.0')

if __name__ == '__main__':
    main()
