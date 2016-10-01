# -*- coding: utf-8 -*-
from Acquisition import aq_inner
from plone import api
from zope.publisher.browser import BrowserView
from plone.memoize.view import memoize
from zope.schema.interfaces import IVocabularyFactory
from zope.component import queryUtility


class SuppliersView(BrowserView):
    """ Provide an overview over all Suppliers
    """

    @memoize
    def view_name(self):
        return self.__name__

    def sort_options(self):
        options = [{'value': 'alphabet',
                    'content': u'Alphabetical'},
                   {'value': 'newest',
                    'content': u'Newest suppliers on top'},
                   ]
        return options

    @memoize
    def suppliers(self):
        ''' The list of my suppliers
        '''
        # determine sorting order (default: alphabetical)
        request = self.request
        sort_by = "sortable_title"
        order = "ascending"
        searchable_text = None

        if request:
            if 'sort' in request:
                if request.sort == "newest":
                    sort_by = "modified"
                    order = "reverse"
            if 'Title' in request:
                searchable_text = request['Title']

        pc = api.portal.get_tool('portal_catalog')

        query = dict(
            portal_type="Supplier",
            sort_on=sort_by,
            sort_order=order,
        )

        if searchable_text:
            query['Title'] = searchable_text + '*'

        brains = pc(query)

        suppliers = []
        vocab = queryUtility(IVocabularyFactory, name='acme.plants')()
        plants = {t.value: t.title for t in vocab}
        for brain in brains:
            my_plants = brain.plant and [
                plants.get(plant, '') for plant in brain.plant] or []
            suppliers.append({
                'id': brain.getId,
                'title': brain.Title,
                'description': ', '.join(my_plants),
                'url': brain.getURL(),
            })
        return suppliers
