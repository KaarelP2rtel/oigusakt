#!/usr/bin/env python3

import xml.etree.ElementTree as ElementTree
from cached_property import cached_property

class BaseElement():
    _ns={'ts':'tyviseadus_1_10.02.2010'}
    def __init__(self,element):
        self._element=element

    def findChild(self,name):
        return self._element.find('ts:{}'.format(name),namespaces=self._ns)

    def attrib(self,name):
        return self._element.attrib.get(name)

class Metaandmed(BaseElement):
    @cached_property
    def valjaandja(self):
        return self.findChild('valjaandja').text

    @cached_property
    def dokumentLiik(self):
        return self.findChild('dokumentLiik').text

    @cached_property
    def tekstiLiik(self):
        return self.findChild('tekstiliik').text

    @cached_property
    def lyhend(self):
        return self.findChild('lyhend').text

    @cached_property
    def dokumentEtapp(self):
        return self.findChild('dokumentEtapp').text

    @cached_property
    def dokumentStaatus(self):
        return self.findChild('dokumentStaatus').text

class Oigusakt(BaseElement):
    def __init__(self,xml):
        self._element=ElementTree.parse(xml).getroot()

    @cached_property
    def id(self):
        return self.attrib('id')

    @cached_property
    def metaandmed(self):
        return Metaandmed(self.findChild('metaandmed'))

