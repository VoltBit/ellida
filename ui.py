#!/usr/bin/python3.5

import os
import sys

sys.path.append(os.path.dirname(__name__))

from ellida import create_app

def main():
    # create an app instance
    app = create_app()

    app.run(debug=True)

if __name__ == '__main__':
    main()
