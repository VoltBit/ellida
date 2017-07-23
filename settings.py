"""
Module used to keep settings such as IP addresses and ports.
"""
class EllidaSettings(object):

    ENGINE_SOCKET = 27999
    MANAGER_SOCKET = 27998
    UI_SCOKET = 27997
    DAEMON_SOCKET = 27990

    ENGINE_ADDR = "192.168.10.4"
    DAEMON_ADDR = "192.168.10.4"
    # ENGINE_ADDR = "192.168.10.7"
    # DAEMON_ADDR = "192.168.10.7"
    # ENGINE_ADDR = "192.168.160.133"
    # DAEMON_ADDR = "192.168.160.133"
