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
    ENGINE_ADDR = "192.168.10.7"
    DAEMON_ADDR = "192.168.10.7"
    # ENGINE_ADDR = "192.168.160.134"
    # DAEMON_ADDR = "192.168.160.134"
    # ENGINE_ADDR = "192.168.160.136"
    # DAEMON_ADDR = "192.168.160.136"

    random_hellos = [
        "Why so silent?!",
        "I miss you...",
        "Say something!",
        "I am still here.",
        "Helooo from the other siiiide!",
    ]

    prov_list = [
        {
            'name': 'Core',
            'desc': 'Core set of standalone tests provided by Ellida',
            'type': 'general',
            'state': 'active'},
        {
            'name':'LTP',
            'desc': 'Linux Test Project',
            'type': 'general',
            'state': 'active'},
        {
            'name': 'LLTng',
            'desc': 'Tracing framework for Linux',
            'type': 'monitor',
            'state': 'inactive'},
        {
            'name': 'Phoronix',
            'desc': 'Benchmarking platform',
            'type': 'benchmark',
            'state': 'inactive'},
        {
            'name': 'Lynis',
            'desc': 'System and security auditing tool',
            'type': 'security',
            'state': 'inactive'},
        {
            'name': 'LDTP',
            'desc': 'Linux Desktop Testing Project',
            'type': 'interface',
            'state': 'inactive'},
        {
            'name': 'Image Tests',
            'desc': 'Yocto package for easy managing and writing pf Python tests',
            'type': 'general',
            'state': 'inactive'}
    ]

    @classmethod
    def random_hello(cls):
        return random.choice(cls.random_hellos)
