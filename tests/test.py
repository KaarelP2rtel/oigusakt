#!/usr/bin/env python3

import unittest
from oigusakt import *

class TestOigusakt(unittest.TestCase):
    def setUp(self):
        testxml='tests/relvaseadus.xml'
        with open(testxml,'r') as xml:
            self.akt = Seadus(xml=xml.read())


    def test_oigusakt_has_id(self):

        self.assertEqual('7bd95b30-0712-4479-b382-c53a8038faf5',self.akt.id)

    def test_oigusakt_has_metaandmed(self):

        self.assertIsInstance(self.akt.metaandmed,Metaandmed)

    def test_oigusakt_metandmed_has_fields(self):
        meta = self.akt.metaandmed
        self.assertEqual('Riigikogu',meta.valjaandja)
        self.assertEqual('seadus',meta.dokumentLiik)
        self.assertEqual('terviktekst',meta.tekstiliik)
        self.assertEqual('RelvS',meta.lyhend)
        self.assertEqual('avaldamine',meta.dokumentEtapp)
        self.assertEqual('avaldatud',meta.dokumentStaatus)

    def test_metaandmed_has_vastuvoetud(self):
        self.assertIsInstance(self.akt.metaandmed.vastuvoetud,Vastuvoetud)
    def test_metaandmed_has_avaldamismarge(self):
        self.assertIsInstance(self.akt.metaandmed.avaldamismarge,Avaldamismarge)

    def test_vastuvoetud_has_fields(self):
        vastuvoetud= self.akt.metaandmed.vastuvoetud
        self.assertEqual('2001-06-13',vastuvoetud.aktikuupaev)
        self.assertEqual('2002-03-31',vastuvoetud.joustumine)

    def test_vastuvoetud_has_avaldamismarge(self):
        self.assertIsInstance(self.akt.metaandmed.vastuvoetud.avaldamismarge,Avaldamismarge)

    def test_vastuvoetud_avaldamismarge_has_fields(self):
        am = self.akt.metaandmed.vastuvoetud.avaldamismarge
        self.assertEqual('RT I',am.RTosa)
        self.assertEqual('2001',am.RTaasta)
        self.assertEqual('65',am.RTnr)
        self.assertEqual('377',am.RTartikkel)
        self.assertEqual('73058',am.aktViide)

    def test_meta_avaldamismarge_has_fields(self):
        am = self.akt.metaandmed.avaldamismarge
        self.assertEqual('RT I',am.RTosa)
        self.assertEqual('2019',am.RTaasta)
        self.assertEqual('80',am.RTartikkel)
        self.assertEqual('119032019080',am.aktViide)
        self.assertEqual('2019-03-19+02:00',am.avaldamineKuupaev)
    def test_meta_has_kehtivus(self):
        self.assertIsInstance(self.akt.metaandmed.kehtivus,Kehtivus)

    def test_meta_kehtivus_has_fields(self):
        kehtivus = self.akt.metaandmed.kehtivus
        self.assertEqual('2020-01-01',kehtivus.kehtivuseAlgus)

    #At this point I decided to skip writing the same test with different names.

    def test_oigusakt_has_name(self):
        self.assertEqual('Relvaseadus',self.akt.aktinimi.nimi.pealkiri )

    def test_oigusakt_has_normtehnmarkus(self):
        self.assertEqual('1',self.akt.aktinimi.nimi.normtehnmarkus.normtehnmarkusNr )
        self.assertIsInstance(self.akt.muutmismarkmed,tuple)
        self.assertIsInstance(self.akt.muutmismarkmed[0],Muutmismarge)

    def test_oigusakt_has_muutmismarkmed(self):
        self.assertEqual(61,len(self.akt.muutmismarkmed))
    def test_muutmismarge_has_fields(self):
        self.assertEqual('531',self.akt.muutmismarkmed[0].avaldamismarge.RTartikkel)
        self.assertEqual(', osaliselt 14.12.2019',self.akt.muutmismarkmed[59].tavatekst)

    def test_akt_has_peatykid(self):
        self.assertEqual(20,len(self.akt.sisu.peatykid))

    def test_peatykk_has_paragrahvs(self):
        self.assertEqual(14,len(self.akt.sisu.peatykid[0].paragrahvid))

    def test_paragrahv_has_loiked(self):
        self.assertEqual(5,len(self.akt.sisu.peatykid[0].paragrahvid[0].loiked))

    def test_tavatekst_may_have_html_sup_tags(self):
        text_with_html="Käesoleva seaduse 8. ja 8<sup>1</sup>. peatükki ei kohaldata teises riigis laskekõlbmatuks muudetud tulirelvale, mis on toodud Eestisse eesmärgiga seda siin püsivalt vallata."
        tavatekst=self.akt.sisu.peatykid[0].paragrahvid[2].loiked[1].sisuTekst.valmistekst
        self.assertEqual(text_with_html,tavatekst)

    def test_tavatekst_may_have_html_tags(self):
        text_with_shitloads_of_html='Tekst<sup>SUPTEKST</sup>Tekst2<i>ITEKST</i>Tekst3<p>PTEKST</p>Tekst4<b>BTEKST</b>Tekst5Tekst<sup>SUPTEKST</sup>Tekst2<i>ITEKST</i>Tekst3<p>PTEKST</p>Tekst4<b>BTEKST</b>Tekst5'
        with open('tests/htmltags.xml','r') as htmlxml:
            tavatekst=Seadus(htmlxml.read()).sisu.peatykid[0].paragrahvid[0].loiked[0].sisuTekst.valmistekst
        self.assertEqual(text_with_shitloads_of_html,tavatekst)
    def test_tavatekst_may_have_self_closing_html_tags(self):
        text_with_self_closing_tag='Tekst<br></br>Tekst'
        with open('tests/reavahetus.xml','r') as htmlxml:
            tavatekst=Seadus(htmlxml.read()).sisu.peatykid[0].paragrahvid[0].loiked[0].sisuTekst.valmistekst
        self.assertEqual(text_with_self_closing_tag,tavatekst)
    def test_tavatekst_may_have_retarded_html_tags(self):
        text_with_reavahetus_tag='Tekst–<br></br>Tekst'
        with open('tests/reavahetus.xml','r') as htmlxml:
            tavatekst=Seadus(htmlxml.read()).sisu.peatykid[0].paragrahvid[0].loiked[1].sisuTekst.valmistekst
        self.assertEqual(text_with_reavahetus_tag,tavatekst)
    def test_akt_may_have_different_namespaces(self):
        with open('tests/maarus.xml','r') as maarus:
            valjaandja = Oigusakt(maarus.read()).metaandmed.valjaandja
            self.assertEqual('Siseminister',valjaandja)
    def test_dangling_paragraphs_are_added_to_last_list(self):
        with open('tests/pere.xml', 'r') as pere:
            osad=Seadus(pere.read()).sisu.osad
        self.assertEqual(12,len(osad[3].paragrahvid))
    def test_sisutekst_tavatekst_is_added_together(self):
        
        expected="esitatavate andmete loetelu kehtestab valdkonna eest vastutav minister määrusega."
        with open('tests/pere.xml', 'r') as pere:
            tavatekst=Seadus(pere.read()).sisu.osad[1].peatykid[5].paragrahvid[11].loiked[2].sisuTekst.valmistekst
        self.assertIn(expected,tavatekst)

if __name__ == '__main__':
    unittest.main()