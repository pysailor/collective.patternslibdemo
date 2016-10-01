# -*- coding: utf-8 -*-

from collective.patternslibdemo import _
from plone.dexterity.content import Container
from plone.directives import form
from zope import schema


class ISupplier(form.Schema):

    title = schema.TextLine(
        title=_(u"Title"),
        required=True,
    )

    description = schema.Text(
        title=_(u"Description"),
        required=False,
    )

    # plant = schema.List(
    #     title=_(u"Plant"),
    #     required=True,
    #     value_type=schema.Choice(
    #         source="acme.plants",
    #     ),
    # )


class Supplier(Container):
    """
        Folderish content type that represents a supplier
    """

    pass
