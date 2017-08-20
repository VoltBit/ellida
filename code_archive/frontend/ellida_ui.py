#!/usr/bin/python3

from sofi.app import Sofi
from sofi.ui import Container, View, Row, Panel, Column, ListGroup, ListItem, Div
from sofi.ui import Paragraph, Heading, Anchor, Image, Label, Span, Textarea, Input
from sofi.ui import Navbar, Dropdown, DropdownItem, UnorderedList
from sofi.ui import Button, ButtonGroup, ButtonToolbar, ButtonDropdown

from colorama import init, Fore
init(autoreset=True)

import zmq
import json
import asyncio
import logging
import os
import sys
import multiprocessing

sys.path.append('/home/smith/Dropbox/')

from ellida.frontend.styles import ButtonStyles
from ellida.settings import EllidaSettings

class EllidaUi(multiprocessing.Process):

    app = None
    # res_path = '../res/'
    res_path = os.path.realpath('res/')
    # res_path = os.path.realpath('../res/')

    spec_list = {'CGL': 'Carrier grade Linux', 'AGL': 'Automotive grade Linux'}
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
            'state': 'inactive'},
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

    # def __init__(self):
    #     self.__network_setup()

    def __network_setup(self):
        self.__context = zmq.Context()
        self.__engine_socket = self.__context.socket(zmq.PAIR)
        self.__engine_socket.connect("tcp://" + EllidaSettings.ENGINE_ADDR + ":" +
                                   str(EllidaSettings.UI_SCOKET))

    @classmethod
    def __gen_nav_interface(cls, current_view):
        interface_elements = []
        top_nav = Navbar(brand="Ellida manager", fixed='top')
        interface_elements.append(top_nav)

        container = Container()
        button_toolbar = ButtonToolbar()
        button_group = ButtonGroup()
        # button_group = ButtonGroup(cl='btn-group-vertical')
        conf_btn = Button('Configuration', severity='primary', size='large',
            ident='conf', style=ButtonStyles.grey_button)
        spec_btn = Button('Specifications', severity='primary',  size='large',
            ident='spec', style=ButtonStyles.grey_button)
        control_btn = Button('Control', severity='primary', size='large',
            ident='control', style=ButtonStyles.grey_button)
        result_btn = Button('Results', severity='primary', size='large',
            ident='result', style=ButtonStyles.grey_button)
        providers_btn = Button('Providers', severity='primary', size='large',
            ident='provider', style=ButtonStyles.grey_button)
        about_btn = Button('About', severity='primary', size='large',
            ident='about', style=ButtonStyles.grey_button)

        menu = Row()
        # menu = Column('md', 2)
        button_group.addelement(conf_btn)
        button_group.addelement(spec_btn)
        button_group.addelement(control_btn)
        button_group.addelement(result_btn)
        button_group.addelement(providers_btn)
        button_group.addelement(about_btn)
        button_toolbar.addelement(button_group)
        menu.addelement(button_toolbar)
        container.addelement(menu)
        interface_elements.append(container)

        for element in interface_elements:
            current_view.addelement(element)
        return current_view

    def __click_msg(self, event):
        if 'id' in event['event_object']['target']:
            # print(event['event_object']['target']['id'] + " CLICKED!")
            # self.__engine_socket.send_string(event['event_object']['target']['id'] + " CLICKED!")
            pass
        else:
            pass
            # print(event['event_object']['target']['innerText'] + " CLICKED!")
            # self.__engine_socket.send_string(event['event_object']['target']['innerText'] + " CLICKED!")

    async def __text_input(self, event):
        if 'id' and 'value' in event['event_object']['target']:
            # print(Fore.BLUE + event['event_object']['target']['id'] + " input value: " +
            #     event['event_object']['target']['value'])
            # self.__engine_socket.send_string(event['event_object']['target']['id'] + " CLICKED!")
            self.__req_input_value = event['event_object']['target']['value']
        else:
            print(Fore.BLUE + event['event_object']['target'].keys())
            # self.__engine_socket.send_string(event['event_object']['target']['innerText'] + " CLICKED!")

    async def __send_req(self, event):
        # print(Fore.BLUE + self.__req_input_value)
        packet = {}
        packet['event'] = "req_exe"
        packet['value'] = self.__req_input_value
        # print(json.dumps(packet))
        self.__engine_socket.send_json(json.dumps(packet))
        # ack = self.__engine_socket.recv_string()

    async def oninit(self, event):
        # Every page is built on top of a View object, which contains the <head> and <body> tags that are filled in by the other objects
        main_view = View("Main")
        main_view = self.__gen_nav_interface(main_view)
        self.app.load(str(main_view), event['client'])
        # config_view = self.__gen_config_view(event)
        # spec_view = self.__gen_spec_view()
        # res_view = self.__gen_result_view()
        # provider_view = self.__gen_providers_view()

    async def onload(self, event):
        self.app.register('click', self.gen_config_view, selector='#conf',
            client=event['client'])
        self.app.register('click', self.gen_spec_view, selector='#spec',
            client=event['client'])
        self.app.register('click', self.gen_control_view, selector='#control',
            client=event['client'])
        self.app.register('click', self.gen_result_view, selector='#result',
            client=event['client'])
        self.app.register('click', self.gen_providers_view, selector='#provider',
            client=event['client'])
        self.app.register('click', self.gen_about_view, selector='#about',
            client=event['client'])
        self.app.register('keyup', self.__text_input, selector='#req_input',
            client=event['client'])
        self.app.register('click', self.__send_req, selector='#req_submit',
            client=event['client'])

    def ui_init(self):
        self.app = Sofi()
        self.app.register('init', self.oninit)
        self.app.register('load', self.onload)
        self.__network_setup()
        self.app.start()

    async def gen_config_view(self, event):
        self.__click_msg(event)
        config_view = View("Configuration")
        config_view = self.__gen_nav_interface(config_view)
        self.app.load(str(config_view), event['client'])
        return config_view

    async def gen_spec_view(self, event):
        # http://jsfiddle.net/Fh47n/
        # http://jsfiddle.net/jhfrench/GpdgF/
        self.__click_msg(event)
        # spec_view = View("Specifications", customcss=["/home/smith/Dropbox/ellida/res/tree.css"],
        spec_view = View("Specifications", customcss=["/home/smith/Dropbox/ellida/res/tree_enhanced.css"],
            customjs=["/home/smith/Dropbox/ellida/res/tree.js"])
        spec_view = self.__gen_nav_interface(spec_view)
        container = Container()
        for spec, descr in self.spec_list.items():
            panel = Panel(heading=True,
                style="max-height:150px; min-height:150px;margin-top:10px;padding-bottom:10px",
                severity='primary')
            panel.setheading(spec + "<div class='pull-right'>" + '+' + "</div>")
            panel.addelement(Paragraph(descr))
            col = Column('md', 4)
            col.addelement(panel)
            container.addelement(col)

        # list_agl_group = ListGroup('Test')
        list_agl = UnorderedList()
        list_agl.addelement(ListItem(str(Span('AGL'))))

        list_agl_os = UnorderedList()
        list_agl_os.addelement(ListItem(str(Span('OS'))))

        list_agl_os_tests = UnorderedList()
        list_agl_os_tests.addelement(ListItem(str(Span('test1'))))
        list_agl_os_tests.addelement(ListItem(str(Span('test1'))))
        list_agl_os_tests.addelement(ListItem(str(Span('test1'))))
        list_agl_os.addelement(list_agl_os_tests)
        list_agl.addelement(list_agl_os)
        agl_tree_top = Div(text=str(list_agl), cl="tree", style="width:350px;margin-left:100px;margin-top:50px")
        # spec_view.addelement(agl_tree_top)


        list_cgl = UnorderedList()
        list_cgl.addelement(ListItem(str(Span('CGL'))))

        list_cgl_os = UnorderedList()
        list_cgl_os.addelement(ListItem(str(Span('OS'))))

        list_cgl_os_tests = UnorderedList()
        list_cgl_os_tests.addelement(ListItem(str(Span('test1'))))
        list_cgl_os_tests.addelement(ListItem(str(Span('test1'))))
        list_cgl_os_tests.addelement(ListItem(str(Span('test1'))))
        list_cgl_os.addelement(list_cgl_os_tests)
        list_cgl.addelement(list_cgl_os)
        cgl_tree_top = Div(text=str(list_cgl), cl="tree", style="width:350px;margin-left:100px;margin-top:50px")

        forest = Row()
        forest.addelement(agl_tree_top)
        forest.addelement(cgl_tree_top)
        spec_view.addelement(forest)
        # spec_view.addelement(list_agl)

        # startpath = "/home/smith/Dropbox/ellida/database/agl"
        # for root, dirs, files in os.walk(startpath):

        #     level = root.replace(startpath, '').count(os.sep)
        #     indent = ' ' * 4 * (level)
        #     print('{}{}/'.format(indent, os.path.basename(root)))
        #     subindent = ' ' * 4 * (level + 1)
        #     for f in files:
        #         print('{}{}'.format(subindent, f))

        self.app.load(str(spec_view), event['client'])
        return spec_view

    async def gen_result_view(self, event):
        self.__click_msg(event)
        res_view = View("Results")
        res_view = self.__gen_nav_interface(res_view)


        progress_bar = Div(
            text=
            """<div class=\"progress-bar\" role=\"progressbar\"
            aria-valuenow=\"70\"
            aria-valuemin=\"0\"
            aria-valuemax=\"100\" style=\"width:70%\">
            AGL 70%</div>""",
            cl="progress",
            style="width: 600px; margin-top: 100px; margin-left: 100px")

        res_view.addelement(progress_bar)
        self.app.load(str(res_view), event['client'])
        return res_view

    async def gen_control_view(self, event):
        self.__click_msg(event)
        control_view = View("Control")
        control_view = self.__gen_nav_interface(control_view)
        container = Container()
        req_area = Row()
        req_input = Input("text", style="width:200px;margin-top:100px;", ident="req_input")
        submit_btn = Button('Submit', severity='primary', size='large',
            ident='req_submit', style=ButtonStyles.grey_button)
        req_area.addelement(req_input)
        req_area.addelement(submit_btn)

        container.addelement(req_area)
        control_view.addelement(container)
        self.app.load(str(control_view), event['client'])
        return control_view

    async def gen_providers_view(self, event):
        self.__click_msg(event)
        provider_view = View("Providers")
        provider_view = self.__gen_nav_interface(provider_view)
        container = Container()
        for provider in self.prov_list:
            panel = Panel(heading=True,
                style="max-height:auto; min-height:150px;margin-top:10px;")
            panel.addelement(Paragraph(provider['desc']))
            ship_icon = Image(cl='pull-right')
            ship_icon.datauri(self.__get_icon_res(provider['type']))
            panel.addelement(ship_icon)

            label = None
            if provider['state'] == 'active':
                label = Label(provider['state'], severity='success')
            elif provider['state'] == 'inactive':
                label = Label(provider['state'], severity='danger')
            panel.setheading(provider['name'] + "<div class='pull-right'>" + str(label) + "</div>")
            # panel.addelement(label)
            col = Column('md', 4)
            col.addelement(panel)
            container.addelement(col)
        provider_view.addelement(container)
        self.app.load(str(provider_view), event['client'])
        return provider_view

    async def gen_about_view(self, event):
        self.__click_msg(event)
        about_view = View("About")
        about_view = self.__gen_nav_interface(about_view)
        self.app.load(str(about_view), event['client'])
        return about_view

    # the way th path is made is wrong because it is relative to the place the script was run
    def __get_icon_res(self, res_type):
        if res_type == 'general':
            return self.res_path + '/viking-ship-black.png'
        if res_type == 'monitor':
            return self.res_path + '/viking-ship-purple.png'
        if res_type == 'benchmark':
            return self.res_path + '/viking-ship-blue.png'
        if res_type == 'security':
            return self.res_path + '/viking-ship-red.png'
        if res_type == 'interface':
            return self.res_path + '/viking-ship-green.png'
        else:
            return self.res_path + '/viking-ship-black.png'

    def shutdown(self):
        self.exit.set()

def main():
    # logging.basicConfig(format="%(asctime)s [%(levelname)s] - %(funcName)s: %(message)s", level=logging.INFO)
    gui = EllidaUi()
    gui.ui_init()

if __name__ == '__main__':
    main()
