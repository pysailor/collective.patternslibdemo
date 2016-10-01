# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import collective.patternslibdemo


class CollectivePatternslibdemoLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=collective.patternslibdemo)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.patternslibdemo:default')


COLLECTIVE_PATTERNSLIBDEMO_FIXTURE = CollectivePatternslibdemoLayer()


COLLECTIVE_PATTERNSLIBDEMO_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_PATTERNSLIBDEMO_FIXTURE,),
    name='CollectivePatternslibdemoLayer:IntegrationTesting'
)


COLLECTIVE_PATTERNSLIBDEMO_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_PATTERNSLIBDEMO_FIXTURE,),
    name='CollectivePatternslibdemoLayer:FunctionalTesting'
)


COLLECTIVE_PATTERNSLIBDEMO_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        COLLECTIVE_PATTERNSLIBDEMO_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='CollectivePatternslibdemoLayer:AcceptanceTesting'
)
