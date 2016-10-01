# -*- coding: utf-8 -*-
from plone import api
from plone.app.dexterity.behaviors.exclfromnav import IExcludeFromNavigation
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent
from zope.publisher.browser import BrowserView
import random

REG_SLIDE_NO = 'collective.patternslibdemo.slide'


class SlideView(BrowserView):

    index = ViewPageTemplateFile('templates/slide.pt')

    def __call__(self):
        slide_no = api.portal.get_registry_record(REG_SLIDE_NO)
        if "form.button.NextSlide" in self.request:
            slide_no += 1
            api.portal.set_registry_record(REG_SLIDE_NO, slide_no)
            action = self.request.get('acme.action', None)
            if action:
                # import pdb; pdb.set_trace( )
                meth = getattr(self, action, None)
                if meth and callable(meth):
                    meth()
        self.slide_no = slide_no
        self.doc = getattr(self.context, str(self.slide_no), None)
        return self.index()

    def show_supplier(self):
        portal = api.portal.get()
        ar = getattr(portal, "audit-reports")
        IExcludeFromNavigation(ar).exclude_from_nav = False
        notify(ObjectModifiedEvent(ar))
        supplier = random.sample(ar.objectValues(), 1)[0]
        self.request.RESPONSE.redirect(supplier.absolute_url())

    def show_suppliers_listing(self):
        self._set_layout_for_ar_folder('suppliers-listing')

    def show_suppliers_listing_injection(self):
        self._set_layout_for_ar_folder('suppliers-listing-injection')

    def show_suppliers_listing_styled(self):
        self._set_layout_for_ar_folder('suppliers-listing-styled')

    def show_audit_search(self):
        self._set_layout_for_ar_folder('audit-search')

    def show_audit_search_filter(self):
        self._set_layout_for_ar_folder('audit-search-filter')

    def show_custom_audit_edit(self):
        setup = api.portal.get_tool('portal_setup')
        setup.runAllImportStepsFromProfile(
            'profile-collective.patternslibdemo:extra')
        portal = api.portal.get()
        ar = getattr(portal, "audit-reports")
        supplier = random.sample(ar.objectValues(), 1)[0]
        audit_report = random.sample(supplier.objectValues(), 1)[0]
        self.request.RESPONSE.redirect(
            "{0}/edit".format(audit_report.absolute_url()))

    def _set_layout_for_ar_folder(self, name):
        portal = api.portal.get()
        ar = getattr(portal, 'audit-reports')
        self._setProp(ar, 'layout', name)
        self.request.RESPONSE.redirect(ar.absolute_url())

    def _setProp(self, obj, name, value):
        if obj.hasProperty(name):
            obj._delProperty(name)
        obj._setProperty(name, value)
