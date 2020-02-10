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
        self.assertEqual('Riigikogu',self.akt.metaandmed.valjaandja)
        self.assertEqual('seadus',self.akt.metaandmed.dokumentLiik)
        self.assertEqual('terviktekst',self.akt.metaandmed.tekstiLiik)
        self.assertEqual('RelvS',self.akt.metaandmed.lyhend)
        self.assertEqual('avaldamine',self.akt.metaandmed.dokumentEtapp)
        self.assertEqual('avaldatud',self.akt.metaandmed.dokumentStaatus)


if __name__ == '__main__':
    unittest.main()