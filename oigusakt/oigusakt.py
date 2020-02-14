#!/usr/bin/env python3

import xml.etree.ElementTree as ElementTree
from cached_property import cached_property

def text(func):
    @cached_property
    def findChildText(context):
        element=context.findChild(func.__name__)
        return element.text if element is not None else None
    return findChildText

def text_with_html_tags(func):
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



def element(func):
    @cached_property
    def findElement(context):
        element = context.findChild(func.__name__)
        return eval(func.__name__.capitalize())(element) if element is not None else None
    return findElement

def element_list(func):
    @cached_property
    def findElement(context):
        name=func(context) #Using the return value of the function as an argument like a boss.
        return tuple(eval(name.capitalize())(i) for i in context.findChildren(name))
    return findElement

def attribute(func):
    @cached_property
    def findAttribute(context):
        return context._element.attrib.get(func.__name__)
    return findAttribute

class BaseElement():
   
    def __init__(self,element):
        self._element=element
        nsAndTag=element.tag.split('}')
        self._tag=nsAndTag.pop()
        ns = nsAndTag.pop().split('{').pop()
        self._ns={'ns':f'{ns}'}

    def findChild(self,name):
        return self._element.find(f'ns:{name}',namespaces=self._ns)

    def findChildren(self,name):
        return self._element.findall(f'ns:{name}',namespaces=self._ns)


    def attrib(self,name):
        return self

    @property
    def tag(self):
        return self._tag


class Oigusakt(BaseElement):
    def __init__(self,xml):
        xmlstring=xml.read().replace('reavahetus','br')
        super().__init__(ElementTree.fromstring(xmlstring))

    @attribute
    def id(self):
        pass

    @element
    def metaandmed(self):
        pass

    @element
    def normtehnmarkus(self):
        pass

    @element
    def aktinimi(self):
        pass


class Seadus(Oigusakt):
         
    @element_list
    def muutmismarkmed(self):
        return 'muutmismarge'

    @element
    def sisu(self):
        pass

    
class Maarus(Oigusakt):
    pass



class Metaandmed(BaseElement):
    @text
    def valjaandja(self):
        pass

    @text
    def dokumentLiik(self):
        pass

    @text
    def tekstiliik(self):
        pass

    @text
    def lyhend(self):
        pass

    @text
    def dokumentEtapp(self):
        pass

    @text
    def dokumentStaatus(self):
        pass

    @element
    def vastuvoetud(self):
        pass
    @element
    def avaldamismarge(self):
        pass
    @element
    def kehtivus(self):
        pass



class Vastuvoetud(BaseElement):
    @text
    def aktikuupaev(self):
        pass

    @text
    def joustumine(self):
        pass

    @element
    def avaldamismarge(self):
        pass

class Avaldamismarge(BaseElement):

    @text
    def RTosa(self):
        pass
    @text
    def RTaasta(self):
        pass
    @text
    def RTnr(self):
        pass
    @text
    def RTartikkel(self):
        pass
    @text
    def aktViide(self):
        pass
    @text
    def avaldamineKuupaev(self):
        pass

class Kehtivus(BaseElement):
    @text
    def kehtivuseAlgus(self):
        pass

class Aktinimi(BaseElement):
    @element
    def nimi(self):
        pass


class Nimi(BaseElement):
    @text
    def pealkiri(self):
        pass
    @element
    def normtehnmarkus(self):
        pass

class Normtehnmarkus(BaseElement):
    @text
    def normtehnmarkusNr(self):
        pass

    @text
    def normtehnmarkusTekst(self):
        pass

    @element
    def muutmismarge(self):
        pass


class Muutmismarge(BaseElement):
    @text
    def aktikuupaev(self):
        pass

    @element
    def avaldamismarge(self):
        pass
    @text
    def joustumine(self):
        pass

    @text_with_html_tags
    def tavatekst(self):
        pass

class Sisu(BaseElement):
    @element_list
    def peatykid(self):
        return 'peatykk'


class Peatykk(BaseElement):
    @attribute
    def id(self):
        pass
    @text
    def peatykkNr(self):
        pass
    @text
    def kuvatavNr(self):
        pass
    @text
    def peatykkPealkiri(self):
        pass

    @element_list
    def paragrahvid(self):
        return 'paragrahv'

    @element_list
    def jaod(self):
        return 'jagu'

class Jagu(BaseElement):
    @attribute
    def id(self):
        pass
    @text
    def jaguNr(self):
        pass
    @text
    def kuvatavNr(self):
        pass
    @text
    def jaguPealkiri(self):
        pass
    @element_list
    def paragrahvid(self):
        return 'paragrahv'



class Paragrahv(BaseElement):
    @attribute
    def id(self):
        pass
    @text
    def kuvatavNr(self):
        pass
    @text
    def paragrahvPealkiri(self):
        pass
    @element
    def sisuTekst(self):
        pass
    @element
    def muutmismarge(self):
        pass

    @element_list
    def loiked(self):
        return 'loige'

class Loige(BaseElement):

    @attribute
    def id(self):
        pass

    @text
    def loigeNr(self):
        pass

    @text
    def kuvatavNr(self):
        pass

    @element
    def muutmismarge(self):
        pass

    @element
    def sisuTekst(self):
        pass

    @element_list
    def alampunktid(self):
        return 'alampunkt'

class Sisutekst(BaseElement):

    @text_with_html_tags
    def tavatekst(self):
        pass

class Alampunkt(BaseElement):

    @attribute
    def id(self):
        pass

    @text
    def alampunktNr(self):
        pass
    @text
    def kuvatavNr(self):
        pass
    @element
    def sisuTekst(self):
        pass
