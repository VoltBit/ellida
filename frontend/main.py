from sofi.app import Sofi
from sofi.ui import Container, View, Row, Panel, Column, ListGroup
from sofi.ui import Paragraph, Heading, Anchor, Image
from sofi.ui import Navbar, Dropdown, DropdownItem
from sofi.ui import Button, ButtonGroup, ButtonToolbar, ButtonDropdown

import json
import asyncio
import logging
from styles import ButtonStyles

class EllidaUI(object):

    app = None

    async def oninit(self, event):
        # Every page is built on top of a View object, which contains the <head> and <body> tags that are filled in by the other objects

        logging.info("Ellida manager started")
        main_view = View("Ellida manager user interface")
        n = Navbar(brand="Ellida manager", fixed='top')
        # n.addlink("Configuration", href='configuration')
        # n.addlink("Specifications")
        # n.addlink("Results")
        # n.addlink("Providers")

        b = Dropdown("Dropdown", align='right')
        b.addelement(DropdownItem('Item Header', header=True))
        b.addelement(DropdownItem('Item 1'))
        b.addelement(DropdownItem('Item 2', disabled=True))
        b.addelement(DropdownItem('', divider=True))
        b.addelement(DropdownItem('Item 3'))

        n.adddropdown(b)
        main_view.addelement(n)

        container = Container()
        button_toolbar = ButtonToolbar()
        button_group = ButtonGroup()
        conf_btn = Button('Configuration', severity='primary', size='large',
            ident='conf', style=ButtonStyles.grey_button)
        spec_btn = Button('Specifications', severity='primary',  size='large',
            ident='spec', style=ButtonStyles.grey_button)
        result_btn = Button('Results', severity='primary', size='large',
            ident='result', style=ButtonStyles.grey_button)
        providers_btn = Button('Providers', severity='primary', size='large',
            ident='provider', style=ButtonStyles.grey_button)

        row_menu = Row()
        list_menu = ListGroup()
        button_group.addelement(conf_btn)
        button_group.addelement(spec_btn)
        button_group.addelement(result_btn)
        button_group.addelement(providers_btn)
        button_toolbar.addelement(button_group)
        row_menu.addelement(button_toolbar)
        container.addelement(row_menu)

        main_view.addelement(container)

        self.app.load(str(main_view), event['client'])

    async def onload(self, event):
        logging.info("LOADED")
        self.app.register('click', self.buttonclicked, selector='#conf',
            client=event['client'])
        self.app.register('click', self.buttonclicked, selector='#spec',
            client=event['client'])
        self.app.register('click', self.buttonclicked, selector='#result',
            client=event['client'])
        self.app.register('click', self.buttonclicked, selector='#provider',
            client=event['client'])

    async def clicked(self, event):
        logging.info("CLICKED!")

    def ui_init(self):

        self.app = Sofi()
        self.app.register('init', self.oninit)
        self.app.register('load', self.onload)
        self.app.register('click', self.clicked)

        self.app.start()

    async def buttonclicked(self, event):
        if ('id' in event['event_object']['target']):
            print(event['event_object']['target']['id'] + " CLICKED!")
            # logging.info("BUTTON " + event['event_object']['target']['id'] + " CLICKED!")
        else:
            # logging.info("BUTTON " + event['event_object']['target']['innerText'] + " CLICKED!")
            print(event['event_object']['target']['innerText'] + " CLICKED!")

def main():
    # logging.basicConfig(format="%(asctime)s [%(levelname)s] - %(funcName)s: %(message)s", level=logging.INFO)
    gui = EllidaUI()
    gui.ui_init()

if __name__ == '__main__':
    main()