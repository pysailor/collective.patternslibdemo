# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from collective.patternslibdemo.testing import COLLECTIVE_PATTERNSLIBDEMO_INTEGRATION_TESTING  # noqa
from plone import api

import unittest


class TestSetup(unittest.TestCase):
    """Test that collective.patternslibdemo is properly installed."""

    layer = COLLECTIVE_PATTERNSLIBDEMO_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if collective.patternslibdemo is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'collective.patternslibdemo'))

    def test_browserlayer(self):
        """Test that ICollectivePatternslibdemoLayer is registered."""
        from collective.patternslibdemo.interfaces import (
            ICollectivePatternslibdemoLayer)
        from plone.browserlayer import utils
        self.assertIn(ICollectivePatternslibdemoLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = COLLECTIVE_PATTERNSLIBDEMO_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['collective.patternslibdemo'])

    def test_product_uninstalled(self):
        """Test if collective.patternslibdemo is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'collective.patternslibdemo'))

    def test_browserlayer_removed(self):
        """Test that ICollectivePatternslibdemoLayer is removed."""
        from collective.patternslibdemo.interfaces import ICollectivePatternslibdemoLayer
        from plone.browserlayer import utils
        self.assertNotIn(ICollectivePatternslibdemoLayer, utils.registered_layers())
