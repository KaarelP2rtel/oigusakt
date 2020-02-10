#!/usr/bin/env python3

import xml.etree.ElementTree as ElementTree
from cached_property import cached_property

def cached_element_text(func):
    @cached_property
    def find(context):
        return context.findChild(func.__name__).text
    return find


class BaseElement():

    _ns={'ts':'tyviseadus_1_10.02.2010'}
    def __init__(self,element):
        self._element=element

    def findChild(self,name):
        return self._element.find('ts:{}'.format(name),namespaces=self._ns)

    def attrib(self,name):
        return self._element.attrib.get(name)


class Oigusakt(BaseElement):
    def __init__(self,xml):
        self._element=ElementTree.parse(xml).getroot()

    @cached_property
    def id(self):
        return self.attrib('id')

    @cached_property
    def metaandmed(self):
        return Metaandmed(self.findChild('metaandmed'))


class Metaandmed(BaseElement):
    @cached_element_text
    def valjaandja(self):
        pass

    @cached_element_text
    def dokumentLiik(self):
        pass

    @cached_element_text
    def tekstiliik(self):
        pass

    @cached_element_text
    def lyhend(self):
        pass

    @cached_element_text
    def dokumentEtapp(self):
        pass

    @cached_element_text
    def dokumentStaatus(self):
        pass

    @cached_property
    def vastuvoetud(self):
        return Vastuvoetud(self.findChild('vastuvoetud'))

class Vastuvoetud(BaseElement):
    @cached_element_text
    def aktikuupaev(self):
        pass

    @cached_element_text
    def joustumine(self):
        pass
