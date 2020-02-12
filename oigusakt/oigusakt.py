#!/usr/bin/env python3

import xml.etree.ElementTree as ElementTree
from cached_property import cached_property


def cached_element_text(func):
    @cached_property
    def findChildText(context):
        element=context.findChild(func.__name__)
        return element.text if element is not None else None
    return findChildText

def cached_element_text_with_html_tags(func):
    @cached_property
    def findChildTextWithHtml(context):
        element=context.findChild(func.__name__)
        if element is not None:
            text=element.text
            for child in element:
                tag = BaseElement(child).tag
                text+=f'<{tag}>{child.text if child.text else ""}</{tag}>{child.tail}'
            return text
        return None
    return findChildTextWithHtml


def cached_element_attribute(func):
    @cached_property
    def findAttribute(context):
        return context._element.attrib.get(func.__name__)
    return findAttribute

def cached_element(func):
    @cached_property
    def findElement(context):
        element = context.findChild(func.__name__)
        return eval(func.__name__.capitalize())(element) if element is not None else None
    return findElement


class BaseElement():

    _ns={'ts':'tyviseadus_1_10.02.2010'}
    def __init__(self,element):
        self._element=element

    def findChild(self,name):
        return self._element.find(f'ts:{name}',namespaces=self._ns)

    def findChildren(self,name):
        return self._element.findall(f'ts:{name}',namespaces=self._ns)


    def attrib(self,name):
        return self

    @cached_property
    def tag(self):
        ns = f'{{{self._ns.get("ts")}}}'
        return self._element.tag.replace(ns,'')

class Oigusakt(BaseElement):
    def __init__(self,xml):
        # Stupid problems call for stupid solutions
        xmlstring=xml.read().replace('reavahetus','br')
        self._element=ElementTree.fromstring(xmlstring)

    @cached_element_attribute
    def id(self):
        pass

    @cached_element
    def metaandmed(self):
        pass

    @cached_element
    def aktinimi(self):
        pass

    @cached_property
    def muutmismarkmed(self):
        return tuple(Muutmismarge(i) for i in self.findChildren('muutmismarge'))

    @cached_element
    def sisu(self):
        pass

    @cached_element
    def normtehnmarkus(self):
        pass



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

    @cached_element
    def vastuvoetud(self):
        pass
    @cached_element
    def avaldamismarge(self):
        pass
    @cached_element
    def kehtivus(self):
        pass



class Vastuvoetud(BaseElement):
    @cached_element_text
    def aktikuupaev(self):
        pass

    @cached_element_text
    def joustumine(self):
        pass

    @cached_element
    def avaldamismarge(self):
        pass

class Avaldamismarge(BaseElement):

    @cached_element_text
    def RTosa(self):
        pass
    @cached_element_text
    def RTaasta(self):
        pass
    @cached_element_text
    def RTnr(self):
        pass
    @cached_element_text
    def RTartikkel(self):
        pass
    @cached_element_text
    def aktViide(self):
        pass
    @cached_element_text
    def avaldamineKuupaev(self):
        pass

class Kehtivus(BaseElement):
    @cached_element_text
    def kehtivuseAlgus(selfl):
        pass

class Aktinimi(BaseElement):
    @cached_element
    def nimi(self):
        pass


class Nimi(BaseElement):
    @cached_element_text
    def pealkiri(self):
        pass
    @cached_element
    def normtehnmarkus(self):
        pass

class Normtehnmarkus(BaseElement):
    @cached_element_text
    def normtehnmarkusNr(self):
        pass

    @cached_element_text
    def normtehnmarkusTekst(self):
        pass

    @cached_element
    def muutmismarge(self):
        pass


class Muutmismarge(BaseElement):
    @cached_element_text
    def aktikuupaev(self):
        pass

    @cached_element
    def avaldamismarge(self):
        pass
    @cached_element_text
    def joustumine(self):
        pass

    @cached_element_text_with_html_tags
    def tavatekst(self):
        pass

class Sisu(BaseElement):
    @cached_property
    def peatykid(self):
        return tuple(Peatykk(i) for i in self.findChildren('peatykk'))


class Peatykk(BaseElement):
    @cached_element_attribute
    def id(self):
        pass
    @cached_element_text
    def peatykkNr(self):
        pass
    @cached_element_text
    def kuvatavNr(self):
        pass
    @cached_element_text
    def peatykkPealkiri(self):
        pass

    @cached_property
    def paragrahvid(self):
        return tuple(Paragrahv(i) for i in self.findChildren('paragrahv'))
    @cached_property
    def jaod(self):
        return tuple(Jagu(i) for i in self.findChildren('jagu'))

class Jagu(BaseElement):
    @cached_element_attribute
    def id(self):
        pass
    @cached_element_text
    def jaguNr(self):
        pass
    @cached_element_text
    def kuvatavNr(self):
        pass
    @cached_element_text
    def jaguPealkiri(self):
        pass
    @cached_property
    def paragrahvid(self):
        return tuple(Paragrahv(i) for i in self.findChildren('paragrahv'))



class Paragrahv(BaseElement):
    @cached_element_attribute
    def id(self):
        pass
    @cached_element_text
    def kuvatavNr(self):
        pass
    @cached_element_text
    def paragrahvPealkiri(self):
        pass
    @cached_element
    def sisuTekst(self):
        pass
    @cached_element
    def muutmismarge(self):
        pass

    @cached_property
    def loiked(self):
        return tuple(Loige(i) for i in self.findChildren('loige'))

class Loige(BaseElement):

    @cached_element_attribute
    def id(self):
        pass

    @cached_element_text
    def loigeNr(self):
        pass

    @cached_element_text
    def kuvatavNr(self):
        pass

    @cached_element
    def muutmismarge(self):
        pass

    @cached_element
    def sisuTekst(self):
        pass

    @cached_property
    def alampunktid(self):
        return tuple(Alampunkt(i) for i in self.findChildren('alampunkt'))
class Sisutekst(BaseElement):

    @cached_element_text_with_html_tags
    def tavatekst(self):
        pass

class Alampunkt(BaseElement):

    @cached_element_attribute
    def id(self):
        pass

    @cached_element_text
    def alampunktNr(self):
        pass
    @cached_element_text
    def kuvatavNr(self):
        pass
    @cached_element
    def sisuTekst(self):
        pass
