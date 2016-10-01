# -*- coding: utf-8 -*-

from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


def plants(context=None):
    terms = [
        SimpleTerm('sherwood', title=u'Sherwood Lumber'),
        SimpleTerm('ivy', title=u'Ivy Greenery'),
        SimpleTerm('grnspn', title=u'Grünspan Copper Works'),
        SimpleTerm('rdgrd', title=u'Rødgrød Explosives'),
    ]
    terms.sort(cmp=lambda x, y: cmp(x.title, y.title))
    return SimpleVocabulary(terms)


def audit_types(context=None):
    terms = [
        SimpleTerm(value="internal", title="Internal"),
        SimpleTerm(value="financial", title="Financial"),
        SimpleTerm(value="operational", title="Operational"),
        SimpleTerm(value="investigative", title="Investigative"),
    ]
    return SimpleVocabulary(terms)


def audit_results(context=None):
    terms = [
        SimpleTerm(value="pass", title="PASS"),
        SimpleTerm(value="conditional", title="COND. PASS"),
        SimpleTerm(value="fail", title="FAIL"),
    ]
    return SimpleVocabulary(terms)


def countries(context=None):
    terms = [
        SimpleTerm("AT", title=u"AT (Austria)"),
        SimpleTerm("AU", title=u"AU (Australia)"),
        SimpleTerm("BE", title=u"BE (Belgium)"),
        SimpleTerm("BR", title=u"BR (Brazil)"),
        SimpleTerm("CH", title=u"CH (Switzerland)"),
        SimpleTerm("CN", title=u"CN (China, People's Republic of)"),
        SimpleTerm("CR", title=u"CR (Costa Rica)"),
        SimpleTerm("CZ", title=u"CZ (Czech Republic)"),
        SimpleTerm("DK", title=u"DK (Denmark)"),
        SimpleTerm("DE", title=u"DE (Germany)"),
        SimpleTerm("ES", title=u"ES (Spain)"),
        SimpleTerm("FR", title=u"FR (France)"),
        SimpleTerm("GR", title=u"GR (Greece)"),
        SimpleTerm("IN", title=u"IN (India)"),
        SimpleTerm("IE", title=u"IE (Ireland)"),
        SimpleTerm("IT", title=u"IT (Italy)"),
        SimpleTerm("JP", title=u"JP (Japan)"),
        SimpleTerm("KR", title=u"KR (Korea, Republic of)"),
        SimpleTerm("MX", title=u"MX (Mexico)"),
        SimpleTerm("NL", title=u"NL (The Netherlands)"),
        SimpleTerm("PT", title=u"PT (Portugal)"),
        SimpleTerm("RO", title=u"RO (Romania)"),
        SimpleTerm("SE", title=u"SE (Sweden)"),
        SimpleTerm("UK", title=u"UK (United Kingdom)"),
        SimpleTerm("US", title=u"US (USA)"),
        SimpleTerm("VN", title=u"VN (Vietnam)"),
    ]
    return SimpleVocabulary(terms)


def wow_states(context=None):
    terms = [
        SimpleTerm("meh", title=u"Meh..."),
        SimpleTerm("ntb", title=u"Not too bad"),
        SimpleTerm("nice", title=u"Pretty good"),
        SimpleTerm("zomg", title=u"Mind-blowing, w00t!")
    ]
    return SimpleVocabulary(terms)
