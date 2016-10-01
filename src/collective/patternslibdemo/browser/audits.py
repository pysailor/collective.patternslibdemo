# -*- coding: utf-8 -*-
from collections import OrderedDict
from DateTime import DateTime
from plone import api
from plone.dexterity.browser.edit import DefaultEditForm
from Products.CMFPlone.browser.search import EVER
from Products.CMFPlone.browser.search import Search
from Products.CMFPlone.browser.search import SortOption
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import queryUtility
from zope.schema.interfaces import IVocabularyFactory
import json
import os


class AuditTypeResults(object):

    audit_results_int_inv = OrderedDict()
    audit_results_int_inv['pass'] = u"A"
    audit_results_int_inv['conditional'] = u"B"
    audit_results_int_inv['fail'] = u"C"
    audit_results_fin = OrderedDict()
    audit_results_fin['pass'] = u"Pass (C)"
    audit_results_fin['conditional'] = u"Cond. Pass (B)"
    audit_results_fin['fail'] = u"Fail (A)"
    audit_results_ops = OrderedDict()
    audit_results_ops['pass'] = u"Green"
    audit_results_ops['conditional'] = u"Yellow"
    audit_results_ops['fail'] = u"Red"
    audit_results = {
        "internal": audit_results_int_inv,
        "investigative": audit_results_int_inv,
        "financial": audit_results_fin,
        "operational": audit_results_ops,
    }

    def audit_result_title(self, audit_type, audit_result):
        result_type = self.audit_results.get(audit_type)
        if result_type:
            return result_type.get(audit_result)


def _make_ordered_dict(mydict):
    keys = mydict.keys()
    keys.sort(cmp=lambda x, y: cmp(x.lower(), y.lower()))
    ordered = OrderedDict()
    for k in keys:
        ordered[k] = mydict[k]
    return ordered


class AuditSearchView(Search):
    """ Provide a complex search interface for autit reports
    """

    def __call__(self):
        # self.on_supplier = ISupplier.providedBy(self.context)
        plant_vocab = queryUtility(IVocabularyFactory, 'acme.plants')()
        self.plant_names = _make_ordered_dict(
            {x.value: x.title for x in plant_vocab})
        self.plant_names_json = json.dumps(self.plant_names)
        audit_vocab = queryUtility(IVocabularyFactory, 'acme.audit_types')()
        self.audit_types = _make_ordered_dict(
            {x.value: x.title for x in audit_vocab})
        self.audit_types_json = json.dumps(self.audit_types)
        countries_vocab = queryUtility(IVocabularyFactory, 'acme.countries')()
        self.countries = _make_ordered_dict(
            {x.value: x.title for x in countries_vocab})
        self.countries_json = json.dumps(self.countries)
        states_vocab = queryUtility(IVocabularyFactory, 'acme.wow_states')()
        self.wow_states = _make_ordered_dict(
            {x.value: x.title for x in states_vocab})
        self.wow_states_json = json.dumps(self.wow_states)
        results_vocab = queryUtility(
            IVocabularyFactory, name="acme.audit_results")(self)
        self.audit_results = {x.value: x.title for x in results_vocab}
        self.audit_results_json = json.dumps(self.audit_results)
        self.filter_active = self.request.get('filter_active', 0)
        self.view_name = self.__name__
        return super(AuditSearchView, self).__call__()

    def results(self, query=None, batch=False, b_size=10, b_start=0,
                use_content_listing=True):
        """ Make sure that the search is always limited to the current context
        """
        if query is None:
            query = {}
        # Make sure that the search is always limited to the current context
        query['path'] = '/'.join(self.context.getPhysicalPath())
        return super(AuditSearchView, self).results(
            query, batch, b_size, b_start, use_content_listing)

    def filter_query(self, query):
        """
        Override default method, so that we can split list-type values
        that come from pat-autosuggest fields by comma into a list
        """
        request = self.request
        if 'from' in self.request and 'to' in self.request:
            query['audit_day'] = {'query': (DateTime(self.request['from']),
                                            DateTime(self.request['to'])),
                                  'range': 'min:max'}

        list_fields = [
            'plant', 'audit_result', 'supplier_location',
            'wow_status']

        catalog = api.portal.get_tool('portal_catalog')
        valid_indexes = tuple(catalog.indexes())
        valid_keys = self.valid_keys + valid_indexes

        text = query.get('SearchableText', None)
        if text is None:
            text = request.form.get('SearchableText', '')
        if not text:
            # Without text, must provide a meaningful non-empty search
            valid = set(valid_indexes).intersection(request.form.keys()) or \
                set(valid_indexes).intersection(query.keys())
            if not valid:
                return

        for k, v in request.form.items():
            if v and ((k in valid_keys) or k.startswith('facet.')):
                if k in list_fields:
                    query[k] = v.split(',')
                else:
                    query[k] = v
        if text:
            query['SearchableText'] = self.munge_search_term(text)

        # don't filter on created at all if we want all results
        created = query.get('created')
        if created:
            try:
                if created.get('query') and created['query'][0] <= EVER:
                    del query['created']
            except AttributeError:
                # created not a mapping
                del query['created']

        query['portal_type'] = u'AuditReport'
        # respect effective/expiration date
        query['show_inactive'] = False

        if 'sort_order' in query and not query['sort_order']:
            del query['sort_order']
        return query

    def default_from(self):
        return DateTime('2000-01-01')

    def default_to(self):
        return DateTime()

    def result_parent_path(self, item):
        return os.path.split(item.getURL())[0]

    def sort_options(self):
        """ Sorting options for search results view. """
        return (
            SortOption(self.request, u'Relevance', ''),
            SortOption(self.request,
                       u'Audit day (newest first)',
                       'audit_day', reverse=True
                       ),
            SortOption(self.request, u'alphabetically', 'sortable_title'),
        )


class AuditReportEditForm(DefaultEditForm, AuditTypeResults):

    template = ViewPageTemplateFile('templates/edit_auditreport.pt')

    def update(self):
        super(AuditReportEditForm, self).update()
