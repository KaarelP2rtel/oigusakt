#!/usr/bin/env python3

import unittest
from oigusakt import *

class TestOigusakt(unittest.TestCase):
    def setUp(self):
        testxml="tests/relvaseadus.xml"
        xml = open(testxml,'r')
        self.akt = Oigusakt(xml=xml)


    def test_oigusakt_has_id(self):

        self.assertEqual("7bd95b30-0712-4479-b382-c53a8038faf5",self.akt.id)

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

    def test_vastuvoetud_has_fields(self):
        vastuvoetud= self.akt.metaandmed.vastuvoetud
        self.assertEqual('2001-06-13',vastuvoetud.aktikuupaev)
        self.assertEqual('2002-03-31',vastuvoetud.joustumine)




if __name__ == '__main__':
    unittest.main()