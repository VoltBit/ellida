"""
Module used to keep settings such as IP addresses and ports.
"""

import random

class EllidaSettings(object):

    ENGINE_SOCKET = 27999
    MANAGER_SOCKET = 27998
    UI_SCOKET = 27997
    DAEMON_SOCKET = 27990

    # DAEMON_ADDR = "192.168.7.2"
    # ENGINE_ADDR = "192.168.10.4"
    # DAEMON_ADDR = "192.168.10.4"
    # ENGINE_ADDR = "192.168.10.7"
    # DAEMON_ADDR = "192.168.10.7"
    # ENGINE_ADDR = "192.168.160.133"
    # DAEMON_ADDR = "192.168.160.133"
    ENGINE_ADDR = "192.168.42.102"
    DAEMON_ADDR = "192.168.42.102"

    random_hellos = [
        "Why so silent?!",
        "I miss you...",
        "Say something!",
        "I am still here.",
        "Helooo from the other siiiide!",
    ]

    @classmethod
    def random_hello(cls):
        return random.choice(cls.random_hellos)
