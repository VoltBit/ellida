from sofi.app import Sofi

# from sofi.ui import Container, Paragraph, Heading, View
import sofi.ui

for i in dir(sofi.ui):
   print (i, "\t\t", type(getattr(sofi.ui, i)))