# -*- coding: utf-8 -*-

from collective import dexteritytextindexer
from collective.patternslibdemo import _
from plone.dexterity.content import Item
from plone.directives import form
from plone.namedfile.field import NamedBlobFile
from plone.rfc822.interfaces import IPrimaryField
from zope import schema
from zope.interface import alsoProvides
import datetime


def audit_day_default():
    return datetime.date.today()


class IAuditReport(form.Schema):

    dexteritytextindexer.searchable('title')
    title = schema.TextLine(
        title=_(u"Title"),
        required=False,
    )

    dexteritytextindexer.searchable('plant')
    plant = schema.Choice(
        title=_(u"Plant"),
        required=True,
        source="acme.plants",
    )

    audit_type = schema.Choice(
        title=_(u"Audit type"),
        required=True,
        source="acme.audit_types",
    )

    audit_day = schema.Date(
        title=_(u"Audit day"),
        required=True,
        defaultFactory=audit_day_default,
    )

    audit_result = schema.Choice(
        title=_("Audit result"),
        required=True,
        source="acme.audit_results",
    )

    supplier_location = schema.Choice(
        title=_("Supplier location"),
        required=True,
        source="acme.countries",
    )

    wow_state = schema.Choice(
        title=_(u'State of "Wow-ness"'),
        description=_(u"How impressive is the supplier's portfolio?"),
        required=True,
        source="acme.wow_states",
    )

    dexteritytextindexer.searchable('part_number')
    part_number = schema.TextLine(
        title=_(u"Part number"),
        required=False,
    )

    file = NamedBlobFile(
        title=_(u"File"),
        required=True,
    )

alsoProvides(IAuditReport['file'], IPrimaryField)


class AuditReport(Item):
    """
        File-base content type that represents an audit report file
    """

    pass
