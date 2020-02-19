#!/usr/bin/env python3

import xml.etree.ElementTree as ElementTree
from cached_property import cached_property
from .xmlmapper import *

def valmistekst(func):
    @cached_property
    def parseText(context):
        text=''
        for i in context._element:
            child=BaseElement(i)
            if child.tag=='tavatekst':
                text+=child._element.text
                for h in child._element:
                    html=BaseElement(h)
                    if html.tag in ['b','i','sup','sub','br','p']:
                        element=html._element
                        text+=f'<{html.tag}>{element.text if element.text else ""}</{html.tag}>{element.tail}'
            elif child.tag=='viide':
                text+=child.findChild('kuvatavTekst').text
        return text
    return parseText

class Kehtivus(BaseElement):
    @date
    def kehtivuseAlgus(self):pass



class Avaldamismarge(BaseElement):

    @text
    def RTosa(self):pass

    @text
    def RTaasta(self):pass

    @text
    def RTnr(self):pass

    @text
    def RTartikkel(self):pass

    @text
    def aktViide(self):pass

    @date
    def avaldamineKuupaev(self):pass

class Vastuvoetud(BaseElement):


    @date
    def aktikuupaev(self):pass

    @date
    def joustumine(self):pass

    @element(Avaldamismarge)
    def avaldamismarge(self):pass

class Muutmismarge(BaseElement):
    @date
    def aktikuupaev(self):pass

    @element(Avaldamismarge)
    def avaldamismarge(self):pass

    @date
    def joustumine(self):pass

    @text_with_html_tags
    def tavatekst(self):pass

    @valmistekst
    def valmistekst(self):pass

    @property
    def valmismarge(self):
        text='['
        for i in self._element:
            child=BaseElement(i)
            if child.tag=='tavatekst':
                text+=child._element.text
                for h in child._element:
                    html=BaseElement(h)
                    if html.tag in ['b','i','sup','sub','br','p']:
                        element=html._element
                        text+=f'<{html.tag}>{element.text if element.text else ""}</{html.tag}>{element.tail}'
            elif child.tag=='viide':
                text+=child.findChild('kuvatavTekst').text
            elif child.tag=='joustumine':
                text += ' - jõust. '
                date=parser.parse(child._element.text.split('+')[0])
                text+= date.strftime('%d.%m.%Y')

            elif child.tag=='avaldamismarge':
                marge=Avaldamismarge(child._element)
                if marge.RTosa:
                    text+=f'{marge.RTosa}, '
                if marge.RTaasta:
                    text+=f'{marge.RTaasta}, '
                elif marge.avaldamineKuupaev:
                    text+=f'{marge.avaldamineKuupaev}, '
                if marge.RTnr:
                    text+= f'{marge.RTnr}, '
                text += marge.RTartikkel


        return text+']'




class Normtehnmarkus(BaseElement):
    @text
    def normtehnmarkusNr(self):pass

    @text
    def normtehnmarkusTekst(self):pass

    @element(Muutmismarge)
    def muutmismarge(self):pass


class Nimi(BaseElement):
    @text
    def pealkiri(self):pass

    @element(Normtehnmarkus)
    def normtehnmarkus(self):pass

class Aktinimi(BaseElement):
    @element(Nimi)
    def nimi(self):pass

class Sisutekst(BaseElement):
    @valmistekst
    def valmistekst(self):pass

class Preambul(BaseElement):
    @valmistekst
    def valmistekst(self):
        pass

class Alampunkt(BaseElement):

    @attribute
    def id(self):pass

    @text
    def alampunktNr(self):pass

    @text
    def kuvatavNr(self):pass

    @element(Sisutekst)
    def sisuTekst(self):pass

    @element(Muutmismarge)
    def muutmismarge(self):pass

class Loige(BaseElement):

    @attribute
    def id(self):pass

    @text
    def loigeNr(self):pass

    @text
    def kuvatavNr(self):pass

    @element(Muutmismarge)
    def muutmismarge(self):pass

    @element(Sisutekst)
    def sisuTekst(self):pass

    @element_list(Alampunkt)
    def alampunktid(self):pass

class Metaandmed(BaseElement):

    @text
    def valjaandja(self):pass

    @text
    def dokumentLiik(self):pass

    @text
    def tekstiliik(self):pass

    @text
    def lyhend(self):pass

    @text
    def dokumentEtapp(self):pass

    @text
    def dokumentStaatus(self):pass

    @element(Vastuvoetud)
    def vastuvoetud(self):pass

    @element(Avaldamismarge)
    def avaldamismarge(self):pass

    @element(Kehtivus)
    def kehtivus(self):pass


class Oigusakt(BaseElement):
    def __init__(self,xml):
        xml=xml\
            .replace('reavahetus','br')\
            .replace('ylaIndeks','sup')\
            .replace('alaIndeks','sub')
        root=self.adoptAbandonedParagraphs(ElementTree.fromstring(xml))
        super().__init__(root)

    @attribute
    def id(self):pass

    @element(Metaandmed)
    def metaandmed(self):
        return Metaandmed

    @element(Normtehnmarkus)
    def normtehnmarkus(self):pass

    @element(Aktinimi)
    def aktinimi(self):pass

    def adoptAbandonedParagraphs(self,root):
        sisu=BaseElement(root).findChild('sisu')
        owner=None
        for i in sisu:
            child = BaseElement(i)
            if child.tag=='paragrahv':
                owner.append(i)
            else:
                owner=i
        return root


class Paragrahv(BaseElement):
    @attribute
    def id(self):pass

    @text
    def kuvatavNr(self):pass

    @text
    def paragrahvPealkiri(self):pass

    @element(Sisutekst)
    def sisuTekst(self):pass

    @element(Muutmismarge)
    def muutmismarge(self):pass

    @element_list(Loige)
    def loiked(self):pass

class Alljaotis(BaseElement):
    @attribute
    def id(self):pass

    @text
    def alljaotisNr(self):pass

    @text
    def alljaotisPealkiri(self):pass

    @text
    def kuvatavNr(self):pass

    @element_list(Paragrahv)
    def paragrahvid(self):pass

    @element(Muutmismarge)
    def muutmismarge(self):pass

class Jaotis(BaseElement):
    @attribute
    def id(self):pass

    @text
    def jaotisNr(self):pass

    @text
    def kuvatavNr(self):pass

    @text
    def jaotisPealkiri(self):pass

    @element_list(Paragrahv)
    def paragrahvid(self):pass

    @element_list(Alljaotis)
    def alljaotised(self):pass

    @element(Muutmismarge)
    def muutmismarge(self):pass


class Jagu(BaseElement):
    @attribute
    def id(self):pass

    @text
    def jaguNr(self):pass

    @text
    def kuvatavNr(self):pass

    @text
    def jaguPealkiri(self):pass

    @element_list(Jaotis)
    def jaotised(self):pass

    @element_list(Paragrahv)
    def paragrahvid(self):pass

    @element(Muutmismarge)
    def muutmismarge(self):pass


class Peatykk(BaseElement):

    @attribute
    def id(self):pass

    @text
    def peatykkNr(self):pass

    @text
    def kuvatavNr(self):pass

    @text
    def peatykkPealkiri(self):pass

    @element_list(Paragrahv)
    def paragrahvid(self):pass

    @element_list(Jagu)
    def jaod(self):pass

    @element(Muutmismarge)
    def muutmismarge(self):pass
class Osa(BaseElement):
    @attribute
    def id(self):pass

    @text
    def osaNr(self):pass

    @text
    def kuvatavNr(self):pass

    @text
    def osaPealkiri(self):pass

    @element_list(Peatykk)
    def peatykid(self):pass

    @element_list(Paragrahv)
    def paragrahvid(self):pass

class SeaduseSisu(BaseElement):
    @element(Preambul)
    def preambul(self):pass

    @element_list(Peatykk)
    def peatykid(self):pass

    @element_list(Osa)
    def osad(self):pass

class MaaruseSisu(BaseElement):
    @element_list(Paragrahv)
    def paragrahvid(self):pass

class Seadus(Oigusakt):

    @element_list(Muutmismarge)
    def muutmismarkmed(self):pass

    @element(SeaduseSisu)
    def sisu(self):pass

class Maarus(Oigusakt):
    @element(MaaruseSisu)
    def sisu(self):pass
