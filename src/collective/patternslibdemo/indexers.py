# -*- coding: utf-8 -*-

from Acquisition import aq_parent
from collective.patternslibdemo.content.auditreport import IAuditReport
from plone.indexer.decorator import indexer
from plone.dexterity.interfaces import IDexterityContent


@indexer(IDexterityContent)
def supplier_title_dexterity(obj):
    """
    dummy to prevent indexing child objects
    """
    raise AttributeError("This field should not indexed here!")


@indexer(IAuditReport)
def supplier_title(obj):
    """
    :return: title of parent, which is a supplier
    """
    return aq_parent(obj).Title()
