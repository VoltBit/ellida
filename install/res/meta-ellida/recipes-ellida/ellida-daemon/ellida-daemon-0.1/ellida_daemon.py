#!/usr/bin/env python
import sys
sys.path.append('/usr/bin/python3.5/site-packages/')
sys.path.append('/usr/bin/python2.7/site-packages/')
from ellidadaemon.daemon import EllidaDaemon

def main():
    ellida_daemon = EllidaDaemon()
    ellida_daemon.daemon_start()

if __name__ == '__main__':
    main()
