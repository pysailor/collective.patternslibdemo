# -*- coding: utf-8 -*-
from datetime import datetime
from datetime import timedelta
from hashlib import md5
from plone import api
from plone.app.dexterity.behaviors.exclfromnav import IExcludeFromNavigation
from plone.namedfile.file import NamedBlobFile
from Products.CMFPlone.interfaces import INonInstallable
from zope.component import queryUtility
from zope.event import notify
from zope.interface import implementer
from zope.lifecycleevent import ObjectModifiedEvent
from zope.schema.interfaces import IVocabularyFactory
import os


@implementer(INonInstallable)
class HiddenProfiles(object):

    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller"""
        return [
            'collective.patternslibdemo:uninstall',
        ]


def post_install(context):
    """Post install script"""
    _configure_ci(context)
    portal = api.portal.get()
    story = getattr(portal, 'the-story', None)
    if story:
        IExcludeFromNavigation(story).exclude_from_nav = False
        notify(ObjectModifiedEvent(story))
    if 'audit-reports' not in portal:
        ar = api.content.create(
            container=portal,
            type="Folder",
            id='audit-reports',
            title='Audit Reports',
        )
        IExcludeFromNavigation(ar).exclude_from_nav = True
    create_content()


def _configure_ci(context):
    """Sets a few ci related attributes"""
    logo_data = """filenameb64:YWNtZV9sb2dvLmdpZg==;datab64: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"""  # noqa
    api.portal.set_registry_record('plone.site_logo', logo_data)


def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.


suppliers_data = {
    'beru_electronics': {'title': u'BERU Electronics'},
    'blackburn_metals': {'title': u'BLACKBURN METALS'},
    'brose_automotive_la_suze_sas': {
        'title': u'BROSE Automotive La Suze SAS.'},
    'btv_plast': {'title': u'BTV plast'},
    'bando_europe': {'title': u'Bando Europe '},
    'basell_polyolefine_gmbh': {'title': u'Basell Polyolefine GmbH'},
    'baylis_automotive': {'title': u'Baylis Automotive'},
    'bradford_rubber': {'title': u'Bradford Rubber'},
    'brookvale': {'title': u'Brookvale'},
    'boellhoff': {'title': u'Böllhoff '},
    'c_brown_sons_steel': {'title': u'C.BROWN & SONS (STEEL) '},
    'crocodile_packaging_crocodile_packaging': {
        'title': u'CROCODILE PACKAGING'},
    'carbody_sas': {'title': u'Carbody S.A.S'},
    'carbody_sealing_safety_solut': {
        'title': u'Carbody Sealing & Safety Solut'},
    'cold_formed_product': {'title': u'Cold Formed Product '},
    'crown_plastic_mouldings': {'title': u'Crown Plastic Mouldings'},
    'ds_smith_packaging': {'title': u'DS SMITH PACKAGING'},
    'dsg-canusa': {'title': u'DSG-CANUSA '},
    'ditter_plastic': {'title': u'Ditter Plastic '},
    'dr_haubitz': {'title': u'Dr. Haubitz '},
    'elval_hellenic_aluminium_ind': {
        'title': u'ELVAL Hellenic Aluminium Ind.'},
    'eaton_eaton': {'title': u'Eaton Eaton'},
    'eaton_areoquip': {'title': u'Eaton Areoquip'},
    'eberspaecher_catem': {'title': u'Eberspächer catem '},
    'epcos': {'title': u'Epcos'},
    'eurofoam_hungary': {'title': u'Eurofoam Hungary'},
    'euronak': {'title': u'Euronak'},
    'flow_dry': {'title': u'FLOW DRY'},
    'forez': {'title': u'FOREZ '},
    'farplas': {'title': u'Farplas'},
    'federal_mogul': {'title': u'Federal Mogul'},
    'fontana': {'title': u'Fontana '},
    'forward_industrial': {'title': u'Forward Industrial'},
}


def create_content():
    portal = api.portal.get()
    ar = portal.get('audit-reports')

    for index, supplier_id in enumerate(suppliers_data):
        # plant1 = some_reg_key(index, 'acme.plants')
        # plant2 = some_reg_key(index + 1, 'acme.plants')
        # plants = (plant1, plant2)
        supplier_title = suppliers_data[supplier_id]['title']
        supplier = api.content.create(
            container=ar,
            type='Supplier',
            id=supplier_id,
            title=supplier_title,
            description=supplier_title + ' Supplier Description',
            # plant=plants,
        )
        for i in range(1, 6):
            create_auditreport(i, supplier)


audit_filename = u'TestAuditFile.docx'
audit_filepath = os.path.join(
    os.path.dirname(__file__), 'tests', audit_filename)
audit_file = open(audit_filepath, 'r')
audit_filedata = audit_file.read()


def create_auditreport(index, supplier):
    number = some_number(str(index) + str(supplier))
    part_number = str(number)[:9]
    test_audit_file = NamedBlobFile(
        data=audit_filedata, filename=audit_filename)
    audit_results = ['pass', 'fail', 'conditional'][number % 3]
    plant = some_reg_key(index, 'acme.plants')
    audit_day = datetime(2015, 11, 26) - timedelta(days=(number % 2000))
    audit_file_id = '{}_{}_audit'.format(plant, part_number)
    title = "{0} {1}".format(plant, audit_day.strftime('%Y%m%d'))
    if audit_file_id not in supplier:
        audit_file = api.content.create(
            container=supplier,
            type='AuditReport',
            id=audit_file_id,
            title=title,
            plant=plant,
            audit_type=some_reg_key(number % index, 'acme.audit_types'),
            audit_day=audit_day,
            supplier_location=some_reg_key(number, 'acme.countries'),
            wow_state=some_reg_key(
                index, 'acme.wow_states'),
            part_number=part_number,
            file=test_audit_file,
            audit_result=audit_results,
        )
        notify(ObjectModifiedEvent(audit_file))


def some_reg_key(seed, vocab_id):
    vocab = queryUtility(IVocabularyFactory, name=vocab_id)()
    return sorted([t.value for t in vocab._terms])[seed % len(vocab)]


def some_number(seed):
    """
    Return a random looking number, to add variety to the test data. For
    example, this helps when testing that searches return a variety of results.

    The output should be deterministic based on the seed, so that tests are
    reproducable.
    """
    hashed = md5(seed)
    hex_string = hashed.hexdigest()[:9]
    int_string = int(hex_string, 16)
    return int_string
